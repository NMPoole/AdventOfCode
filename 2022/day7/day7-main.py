#######################################################################################################################
# Advent of Code 2022 - Day 7
#######################################################################################################################

class DTree:
    """
    Directory Tree: class where a member is a directory containing files and possibly other directories (also DTrees)
    """

    def __init__(self, name, parent=None):
        """
        Initialize member of directory tree, giving a name to dir and linking possible parent

        :param name: Name of this directory as member of directory tree
        :param parent: Parent directory of this directory (root has None parent)
        """
        self.name = name
        self.children = {}
        self.files = {}
        self.parent = parent

    def touch(self, size, name):
        """
        Add new file to current dir with given name and size

        :param size: Size of file
        :param name: Name of file
        """
        self.files[name] = int(size)

    def mkdir(self, name):
        """
        Add new directory within curr dir with given name and link curr dir as its parent

        :param name: Name of new dir
        :return: DTree - The new directory member
        """
        return self.children.setdefault(name, DTree(name, parent=self))

    @property
    def root(self):
        """
        Get the root of the DTree by following parents to top level (i.e., root)

        :return: DTree - Root dir
        """
        return self if self.parent is None else self.parent.root

    @property
    def size(self):
        """
        Size of this dir is the sum of all its file sizes, plus the sum of all file sizes in its child directories

        :return: Size of this dir, as defined
        """
        return sum(self.files.values()) + sum(c.size for c in self.children.values())

    def __iter__(self):
        """
        Iterate over DTree depth-first (i.e., visit each child dir of curr dir before moving onto any sibling dirs)

        :return: DTree - Next dir member being iterated over
        """
        for child in self.children.values():
            yield child
            yield from child


def main():
    data = open("day7-input.txt").read().strip().split("\n")  # Read input data as array of lines/instructions

    cwd = DTree("/")  # Initialise directory tree by moving into root, '/'
    for line in data[1:]:
        if line.startswith("dir") or line.startswith("$ ls"):
            continue  # Can ignore - dirs are picked up by cd targets and no need to print cwd with ls
        elif line.startswith("$ cd"):
            target = line[5:]  # Rest of line after '$ cd', i.e., what to cd into
            cwd = cwd.parent if target == ".." else cwd.mkdir(target)  # Navigate to parent or implicit dir creation
        else:  # Adding file of given file size
            size, name = line.split()
            cwd.touch(size, name)

    # Part 1:
    # Note that this sum will re-count file sizes as child dirs are traversed - this is expected in the question!
    part1_sol = sum(curr_dir.size for curr_dir in cwd.root if curr_dir.size < 100000)
    print(f"Find all of the directories with a total size of at most 100000."
          f"\nWhat is the sum of the total sizes of those directories?"
          f"\nAnswer: {part1_sol}")  # part 1

    # Part 2:
    file_system_size = 70000000
    update_size = 30000000
    max_usage = file_system_size - update_size
    part2_sol = min(curr_dir.size for curr_dir in cwd.root if cwd.root.size - curr_dir.size < max_usage)
    print(f"Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update."
          f"\nWhat is the total size of that directory?"
          f"\nAnswer: {part2_sol}")


if __name__ == "__main__":
    main()
