"""
Test suite for git-cl command.
"""

import os


class TestGitCl:
    """Test cases for git-cl command."""

    def test_clone_with_repository_url(self, temp_repo, script_path):
        """Test cloning a repository with a URL."""

        git = temp_repo.git()

        # Create a bare repository to clone from.
        source_repo_path = os.path.join(temp_repo.cwd(), "source.git")
        git.init("--bare", source_repo_path)

        # Clone the repository.
        result = temp_repo.run(script_path, source_repo_path, "cloned")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        cloned_repo_path = os.path.join(temp_repo.cwd(), "cloned")
        assert os.path.isdir(cloned_repo_path)

        # Verify it's a Git repository.
        assert os.path.isdir(os.path.join(cloned_repo_path, ".git"))

    def test_clone_with_depth_option(self, temp_repo, script_path):
        """Test cloning with --depth option."""

        git = temp_repo.git()

        # Create a source repository.
        source_repo_path = os.path.join(temp_repo.cwd(), "source")
        os.makedirs(source_repo_path)
        os.chdir(source_repo_path)
        git.init(source_repo_path)
        git.config("--local", "user.name", "Test User")
        git.config("--local", "user.email", "test@example.com")

        # Create multiple commits in the source repository.
        for i in range(3):
            temp_repo.write(f"file{i}.txt", f"content{i}")
            git.add(f"file{i}.txt")
            git.commit("-m", f"Commit {i}")

        # Return to the original working directory.
        os.chdir(temp_repo.cwd())

        # Clone with depth 1.
        result = temp_repo.run(script_path, "--depth", "1", source_repo_path, "shallow")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        cloned_repo_path = os.path.join(temp_repo.cwd(), "shallow")
        assert os.path.isdir(cloned_repo_path)

    def test_clone_with_single_branch_option(self, temp_repo, script_path):
        """Test cloning with --single-branch option."""

        git = temp_repo.git()

        # Create a source repository.
        source_repo_path = os.path.join(temp_repo.cwd(), "source")
        os.makedirs(source_repo_path)
        os.chdir(source_repo_path)
        git.init(source_repo_path)
        git.config("--local", "user.name", "Test User")
        git.config("--local", "user.email", "test@example.com")

        # Create an initial commit in the source repository.
        temp_repo.write("file.txt", "content")
        git.add("file.txt")
        git.commit("-m", "Initial commit")

        # Return to the original working directory.
        os.chdir(temp_repo.cwd())

        # Clone with single-branch option.
        result = temp_repo.run(
            script_path, "--single-branch", source_repo_path, "single-branch-clone"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        cloned_repo_path = os.path.join(temp_repo.cwd(), "single-branch-clone")
        assert os.path.isdir(cloned_repo_path)

    def test_clone_with_multiple_options(self, temp_repo, script_path):
        """Test cloning with multiple options forwarded."""

        git = temp_repo.git()

        # Create a source repository.
        source_repo_path = os.path.join(temp_repo.cwd(), "source")
        os.makedirs(source_repo_path)
        os.chdir(source_repo_path)
        git.init(source_repo_path)
        git.config("--local", "user.name", "Test User")
        git.config("--local", "user.email", "test@example.com")

        # Create multiple commits in the source repository.
        for i in range(5):
            temp_repo.write(f"file{i}.txt", f"content{i}")
            git.add(f"file{i}.txt")
            git.commit("-m", f"Commit {i}")

        # Return to the original working directory.
        os.chdir(temp_repo.cwd())

        # Clone with multiple options: --depth and --no-tags.
        result = temp_repo.run(
            script_path, "--depth", "2", "--no-tags", source_repo_path, "multi-option"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        cloned_repo_path = os.path.join(temp_repo.cwd(), "multi-option")
        assert os.path.isdir(cloned_repo_path)

    def test_clone_without_arguments(self, temp_repo, script_path):
        """Test that git-cl without arguments fails appropriately."""

        result = temp_repo.run(script_path)

        # Verify error exit code - 'git clone' will fail without arguments.
        assert result.returncode != 0

    def test_clone_with_invalid_repository(self, temp_repo, script_path):
        """Test cloning an invalid repository URL."""

        result = temp_repo.run(script_path, "nonexistent-repo")

        # Verify error exit code.
        assert result.returncode != 0
