import os
import zipfile
import tempfile
import shutil
from django.http import HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from voidcms.helpers.isAdmin import IsAdminUser
from django.utils import timezone
from django.core.management import call_command
from django.db import connection, transaction

# Define the directory where backups will be stored
backup_dir = os.path.join(settings.BASE_DIR, 'backup')
os.makedirs(backup_dir, exist_ok=True)

#Define Models to backup 
exclude_models = '--exclude auth.permission --exclude contenttypes --exclude authtoken.Token'

class BackupView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        if self.request.method in ["GET", "POST", "DELETE", "PUT", "PATCH"]:
            return [IsAdminUser()]
        else:
            return super().get_permissions()

    def get(self, request):
        # Create a temporary directory to store the backup files
        temp_dir = tempfile.mkdtemp(dir=backup_dir)

        # Backup the database using Django's dumpdata management command
        db_backup_file = os.path.join(temp_dir, 'db_backup.json')
        os.system(
            f"python {settings.BASE_DIR}/manage.py dumpdata {exclude_models} > {db_backup_file}")

        # Zip the media folder and add it to the temporary directory
        media_backup_file = os.path.join(temp_dir, 'media_backup.zip')

        with zipfile.ZipFile(media_backup_file, 'w', zipfile.ZIP_DEFLATED) as media_zip:
            media_root = settings.MEDIA_ROOT
            for foldername, subfolders, filenames in os.walk(media_root):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    arcname = os.path.relpath(filepath, media_root)
                    media_zip.write(filepath, arcname=arcname)

        # Create a zip file containing both the database and media backups
        backup_filename = f'backup.zip'
        backup_file_path = os.path.join(backup_dir, backup_filename)
        with zipfile.ZipFile(backup_file_path, 'w', zipfile.ZIP_DEFLATED) as final_zip:
            final_zip.write(db_backup_file, arcname='db_backup.json')
            final_zip.write(media_backup_file, arcname='media_backup.zip')

        # Clean up: Delete the temporary directory and its contents after 2 hours
        cleanup_time = timezone.now() + timezone.timedelta(minutes=60)
        self.cleanup_temp_directory(temp_dir, cleanup_time)
        # self.schedule_cleanup_backup(backup_file_path, cleanup_time)

        # Open the backup file for reading and create a response with it
        with open(backup_file_path, 'rb') as backup_file:
            response = HttpResponse(
                backup_file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{backup_filename}"'
            return response

    def post(self, request):
        # Extract the uploaded ZIP file
        uploaded_file = request.FILES.get('backup_file')
        if not uploaded_file:
            return HttpResponse(status=400, content="No backup file provided")

        # Define the path to a temporary directory to extract the backup
        temp_dir = tempfile.mkdtemp(dir=backup_dir)

        try:
            # Save the uploaded file to the temporary directory
            uploaded_file_path = os.path.join(temp_dir, 'uploaded_backup.zip')
            with open(uploaded_file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Extract the ZIP file
            with zipfile.ZipFile(uploaded_file_path, 'r') as zipf:

                # Restore the database using Django's loaddata management command
                db_backup_file = os.path.join(temp_dir, 'db_backup.json')
                media_backup_file = os.path.join(temp_dir, 'media_backup.zip')

                with zipf.open('db_backup.json') as db_backup:
                    with open(db_backup_file, 'wb') as db_dest:
                        shutil.copyfileobj(db_backup, db_dest)

                with zipf.open('media_backup.zip') as media_backup:
                    with open(media_backup_file, 'wb') as media_dest:
                        shutil.copyfileobj(media_backup, media_dest)

                # Restore the database
                call_command('loaddata', db_backup_file)

                # Restore the media files
                with zipfile.ZipFile(media_backup_file, 'r') as media_zip:
                    media_root = settings.MEDIA_ROOT
                    media_zip.extractall(path=media_root)

        finally:
            # Clean up: Delete the temporary directory and its contents
            shutil.rmtree(temp_dir)

        # Return a response indicating successful restore
        return HttpResponse("Restore successful", status=200)

    def cleanup_temp_directory(self, temp_dir, cleanup_time):
        """
        Cleanup the temporary directory and its contents if it's older than the cleanup_time.
        """
        if os.path.exists(temp_dir):
            dir_mtime = timezone.datetime.fromtimestamp(
                os.path.getmtime(temp_dir), tz=timezone.utc)
            if dir_mtime < cleanup_time:
                shutil.rmtree(temp_dir)
