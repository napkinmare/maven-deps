#!/usr/bin/python3

# Convert gradle cache to a repository and pack into a file on desktop

from datetime import datetime
import os
import hashlib
import tarfile

GRADLE_CACHE_PATH = "/home/user/.gradle/caches/modules-2/files-2.1/"


def sha1sum(path):
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()

    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    return format(sha1.hexdigest())


def main():
    walk_dir = GRADLE_CACHE_PATH

    # Hack - truncate files.txt
    with open(os.path.join(walk_dir, "files.txt"), 'w') as hashes:
        pass

    with open(os.path.join(walk_dir, "files.txt"), 'r') as hashes:
        hash_list = hashes.read().split(",")
        print("number of hashes to skip: {}".format(len(hash_list)))

    with tarfile.open("/home/user/Desktop/{}.tar.gz".format(datetime.now().strftime("%d%m%Y_%H%M%S")), "w|gz") as archive:
        count = 0
        for root, subdirs, files in os.walk(walk_dir):
            dir_name = os.path.basename(root)

            if len(files) == 1:
                file_name = files[0]
                file_path = os.path.join(root, file_name)

                sha1 = sha1sum(file_path)

                # Condition doesn't always work, for example, when '0' + dir_name == sha1
                #if (dir_name == sha1 or dir_name == sha1+"0") and dir_name not in hash_list:
                if True:
                    hash_list.append(dir_name)

                    relative_path = os.path.relpath(file_path, walk_dir)
                    original_path = relative_path.replace("/{}".format(dir_name), "")

                    path_list = os.path.normpath(original_path).split(os.sep)
                    path_list[0] = path_list[0].replace(".", os.sep)
                    archive_path = os.path.join(*path_list)

                    print("[{}]\tArchiving {}...".format(count, archive_path))

                    archive.add(file_path, arcname=archive_path)
                    count += 1

                    continue
    with open("files.txt", 'w') as f:
        f.write(",".join(hash_list))
        print("number of hashes in cache: {}".format(len(hash_list)))


if __name__ == "__main__":
    main()
