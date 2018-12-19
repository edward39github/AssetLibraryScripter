import rarfile
import zipfile
import tarfile
import os

PATH_TO_UNRAREXE = "C:/Program Files/WinRAR/UnRAR.exe"
rarfile.UNRAR_TOOL = PATH_TO_UNRAREXE


class ArchiveFileManager(object):

    # Archive types

    RAR = 'rar'
    ZIP = 'zip'
    TAR = "tar"
    NOT_ARCHIVE = ""


    @staticmethod
    def isArchive(filepath):
        """
        If file path is archive return True, otherwise False

        :param filepath: path to archive file

        :return: bool
        """

        if not isinstance(filepath, str):
            raise TypeError("Expected string")

        if zipfile.is_zipfile(filepath): return True

        if rarfile.is_rarfile(filepath): return True

        return False


    @staticmethod
    def archiveType(filepath):
        """
        Determine archive type

        :param filepath: path to archive file

        :return: archive type Archives.RAR/Archives.ZIP/Archives.NOT_ARCHIVE
        """

        if zipfile.is_zipfile(filepath): return ArchiveFileManager.ZIP

        if rarfile.is_rarfile(filepath): return ArchiveFileManager.RAR

        return ArchiveFileManager.NOT_ARCHIVE


    @staticmethod
    def isRarArchive(filepath):
        """
        Return True if is .rar archive, otherwise False
        :return: bool
        """
        return  rarfile.is_rarfile(filepath)


    @staticmethod
    def isZipArchive(filepath):
        """
        Return True if is .zip archive, otherwise False
        :return: bool
        """
        return zipfile.is_zipfile(filepath)



    def __init__(self):
        super(ArchiveFileManager, self).__init__()
        """
        Provide archive file management. 
        Supported types [".rar", ".zip"]
        """

        self._archiveFile = ""
        self._archive = None
        self._isOpened = False
        self._isBinded = False



    @property
    def archiveFile(self):
        return self._archiveFile


    @property
    def isOpened(self):
        return self._isOpened


    @property
    def isBinded(self):
        return self._isBinded


    @archiveFile.setter
    def archiveFile(self, archiveFile):

        if not isinstance(archiveFile, str):
            raise TypeError("Expected string")

        self._archiveFile = archiveFile
        self._isBinded = True




    def open(self):
        """
        Open archive file

        :return: bool True if opened
        """
        if zipfile.is_zipfile(self._archiveFile):
            self._archive = zipfile.ZipFile(self._archiveFile, "r")
            self._isOpened = True
            return True

        if rarfile.is_rarfile(self._archiveFile):
            self._archive = rarfile.RarFile(self._archiveFile, "r")
            self._isOpened = False
            return True

        return False


    def close(self):
        """
        Close opened archive file
        """
        if self._archive != None:
            self._isOpened = False
            self._archive.close()


    def clear(self):
        self.close()
        self._archive = None
        self._archiveFile = ""
        self._isBinded = False


    def content(self, extensionFilter=[]):
        """
        Return content of archive

        :param extensionFilter: list of supported file extensions (i.e. ["jpg", "fbx", ""].
                        if filter is empty, all file extensions are supported

        :return: list<str>
        """

        if self._archive == None:
            raise StandardError("Archive was not open")

        names = self._archive.namelist()


        content = []
        if extensionFilter:
            for name in names:
                extension = os.path.splitext(name)[-1]
                try:
                    extension = extension[1:]
                    extension = extension.lower()
                except:
                    pass
                if extension in extensionFilter:
                    content.append(name)
        else:
            for name in names:
                content.append(name)

        return content


    def extractAll(self, directory):
        """
        Extract all archive content in "directory"

        :param directory: destination path to extract
        """
        if self._archive == None:
            raise StandardError("Archive was not open")

        self._archive.extractall(directory)


    def extractMember(self, directory, name):
        """
        Extract archive member in "directory"

        :param directory: destination path to extract
        :param name: name of member to extract

        """
        if self._archive == None:
            raise StandardError("Archive was not open")

        self._archive.extract(name, directory)


    def extractMembers(self, directory, names):
        """
        Extract any archive members in "directory"

        :param directory: destination path to extract
        :param names: list of member names to extract

        """
        if self._archive == None:
            raise StandardError("Archive was not open")

        self._archive.extractall(directory, names)


    def extract(self, directory, namemap):
        """
        Extract files from archive and rename them

        :param directory: destination directory path

        :param namemap: map for extractable name map { archive_member_name: new_name }.
                        new name can be with no extension, if new name is empty, member
                        will not be extracted

        """

        if self._archive == None:
            raise StandardError("Archive was not open")


        for name in namemap:
            new_name = namemap[name]
            extension = os.path.splitext(name)[-1]

            if new_name == "":
                new_name = name

            self._archive.extract(name, directory)

            if new_name != name:
                os.rename(
                    os.path.join(directory, name),
                    os.path.join(directory, new_name + extension)
                )




if __name__ == '__main__':

    testdir = "C:/Users/edward/Desktop/archtest"

    rardstdir = os.path.join(testdir, "extract_rar")
    zipdstdir = os.path.join(testdir, "extract_zip")

    rarpath = os.path.join(testdir, "Andesite.rar")
    zippath = os.path.join(testdir, "Debris.zip")

    manager = ArchiveFileManager()

    targz = "C:/Users/edward/Desktop/openexr-2.3.0.tar.gz"
    #manager.archiveFile = "C:/Users/edward/Desktop/openexr-2.3.0.tar.gz"
    #print manager.isArchive(targz)


    # tar.open()

    # print tar.getnames()


    # name = "Dbrs_wood_twig_T_ojDlND_4K_Albedo.jpg"
    # names = manager.content(["fbx"])
    # namesmap = {
    #     "Dbrs_wood_twig_T_ojDlND_4K_Albedo.jpg": "albedo",
    #     "Debris_Wood_Twig_ojDlND_3d_Preview.png": "preview"
    # }


    # manager.extract(zipdstdir, name=name)
    # manager.extract(zipdstdir, names=names)
    #manager.extract(zipdstdir, namesmap=namesmap)

    # manager.archiveFile = rarpath
    # manager.extract(rardstdir)
