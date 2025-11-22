"""
Test suite for git-cl command.
"""

import os


class TestGitCl:
    """Test cases for git-cl command."""

    def test_clone_with_repository_url(self, test_repo, script_path):
        """Test cloning a repository with a URL."""

        # Create a bare repository to clone from.
        source_repo_path = os.path.join(test_repo.cwd(), "source.git")
        test_repo.git.init("--bare", source_repo_path)

        # Clone the repository.
        result = test_repo.run(script_path, source_repo_path, "cloned")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        cloned_repo_path = os.path.join(test_repo.cwd(), "cloned")
        assert os.path.isdir(cloned_repo_path)

        # Verify it's a Git repository.
        assert os.path.isdir(os.path.join(cloned_repo_path, ".git"))

    def test_clone_with_depth_option(self, test_repo, script_path):
        """Test cloning with --depth option."""

        # Create a source repository.
        source_repo_path = os.path.join(test_repo.cwd(), "source")
        os.makedirs(source_repo_path)
        os.chdir(source_repo_path)
        test_repo.git.init(source_repo_path)
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create multiple commits in the source repository.
        for i in range(3):
            test_repo.write(f"file{i}.txt", f"content{i}")
            test_repo.git.add(f"file{i}.txt")
            test_repo.git.commit("-m", f"Commit {i}")

        # Return to the original working directory.
        os.chdir(test_repo.cwd())

        # Clone with depth 1.
        result = test_repo.run(script_path, "--depth", "1", source_repo_path, "shallow")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        cloned_repo_path = os.path.join(test_repo.cwd(), "shallow")
        assert os.path.isdir(cloned_repo_path)

    def test_clone_with_single_branch_option(self, test_repo, script_path):
        """Test cloning with --single-branch option."""

        # Create a source repository.
        source_repo_path = os.path.join(test_repo.cwd(), "source")
        os.makedirs(source_repo_path)
        os.chdir(source_repo_path)
        test_repo.git.init(source_repo_path)
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create an initial commit in the source repository.
        test_repo.write("file.txt", "content")
        test_repo.git.add("file.txt")
        test_repo.git.commit("-m", "Initial commit")

        # Return to the original working directory.
        os.chdir(test_repo.cwd())

        # Clone with single-branch option.
        result = test_repo.run(
            script_path, "--single-branch", source_repo_path, "single-branch-clone"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        cloned_repo_path = os.path.join(test_repo.cwd(), "single-branch-clone")
        assert os.path.isdir(cloned_repo_path)

    def test_clone_with_multiple_options(self, test_repo, script_path):
        """Test cloning with multiple options forwarded."""

        # Create a source repository.
        source_repo_path = os.path.join(test_repo.cwd(), "source")
        os.makedirs(source_repo_path)
        os.chdir(source_repo_path)
        test_repo.git.init(source_repo_path)
        test_repo.git.config("--local", "user.name", "Test User")
        test_repo.git.config("--local", "user.email", "test@example.com")

        # Create multiple commits in the source repository.
        for i in range(5):
            test_repo.write(f"file{i}.txt", f"content{i}")
            test_repo.git.add(f"file{i}.txt")
            test_repo.git.commit("-m", f"Commit {i}")

        # Return to the original working directory.
        os.chdir(test_repo.cwd())

        # Clone with multiple options: --depth and --no-tags.
        result = test_repo.run(
            script_path, "--depth", "2", "--no-tags", source_repo_path, "multi-option"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        cloned_repo_path = os.path.join(test_repo.cwd(), "multi-option")
        assert os.path.isdir(cloned_repo_path)

    def test_clone_without_arguments(self, test_repo, script_path):
        """Test that git-cl without arguments fails appropriately."""

        result = test_repo.run(script_path)

        # Verify error exit code - 'git clone' will fail without arguments.
        assert result.returncode != 0

    def test_clone_with_invalid_repository(self, test_repo, script_path):
        """Test cloning an invalid repository URL."""

        result = test_repo.run(script_path, "nonexistent-repo")

        # Verify error exit code.
        assert result.returncode != 0
