import os
import sys
import glob
from time import sleep
from datetime import datetime
from jobcontrol import Job
from export.noaa import NoaaCycle
import tarfile
import tempfile
import filecmp

class ArchiveJob(Job):
    """
    Put downloaded METAR files in .tar.gz files monthly
    """
    extension = '.tar.gz'
    def action(self):
        files = self.listFiles()
        if not files:
            self.log.info("Nothing to archive for %s" % current_month)
        try:
            archive = self.archive(files, self.archive_name)
            self.cleanup(archive, files)
        except RuntimeError as e:
            self.log.error("Failed to create an archive %s" % archive_name)
            raise

    def listFiles(self):
        """
        Get the list of files to be archived
        """
        current_month = NoaaCycle.last_month()
        # 2do archive contain extra path: data/noaa/metar/2011-* ; better is 2011-*
        dir_regex    = os.path.join(self.download_dir, "%s-*" % current_month)
        self.archive_name = os.path.join(self.download_dir, current_month)
        return glob.glob(dir_regex)

    def configure(self):
        Job.configure(self, 'conf/noaajob.conf')
        self.download_dir = self.config.get("noaajob", "download_dir")

    def archive(self, files, name):
        """
        Put the files into archive; return archive file name
        """
        self.log.debug("Putting files into archive: %s" % "\n".join(files))
        tar_name = "%s%s" % (name, self.extension)
        if os.path.exists(tar_name):
            raise RuntimeError ("Tried to create an archive that already exists: %s" % tar_name) 
        else:
            self.log.info("Creating a new archive %s" % tar_name)
        tar = tarfile.open(tar_name, 'w:gz');
        for name in files:
            tar.add(name)
            print '%s'% (name)
        tar.close()
        return tar_name

    def cleanup(self, archive, files):
        """
        Move the archived files to backup (paranoid version)
        """
        mtime = self.test(archive, files)
        backup_home = os.path.join(self.download_dir, '-')
        if not os.path.exists(backup_home):
            os.makedirs(backup_home)
        backup_dir = tempfile.mkdtemp('', datetime.utcnow().strftime("%Y-%m-%d_"), backup_home)
        for file in files:
            os.makedirs(os.path.join(backup_dir, file))
            if os.path.getmtime(file) != mtime[file]:
                raise RuntimeError("Failed to cleanup archived data: %s has been modified." % file)
            os.rename(file, os.path.join(backup_dir, file))
            self.log.debug("Moved %s to %s" % (file, os.path.join(backup_dir, file)))
        return

    def test(self, archive, files):
        """
        Test the archive; return mtime of each item
        """
        self.log.info("Opening archive %s for testing." % (archive))
        tmpdir = tempfile.mkdtemp(dir='/tmp/')
        tar = tarfile.open(archive, 'r:gz')
        tar.extractall(tmpdir);
        tar.close()

        mtime = {}
        for file in files:
            mtime[file] = os.path.getmtime(file)
            # compare each file to its archived copy
            self.log.debug("Comparing files %s and %s" % (file, tmpdir))
            diffdir = filecmp.dircmp(file, os.path.join(tmpdir, file));
            diffdir.report_full_closure();
            status = {}
            for i in ('left_only', 'right_only', 'diff_files'):
                if len(diffdir.__dict__[i]) > 0:
                    status[i] = len(diffdir.__dict__[i])
            if len(status) > 0:
                raise RuntimeError ("Archive contents do not match source files.")
        return mtime
