"""
Test suite for git-cl command.
"""

import os


class TestGitCl:
    """Test cases for git-cl command."""

    def test_clone_with_repository_url(self, repo, bin):
        """Test cloning a repository with a URL."""

        # Create a bare repository to clone from.
        source_repo_path = os.path.join(repo.cwd(), "source.git")
        repo.git.init("--bare", source_repo_path)

        # Clone the repository.
        result = repo.run(bin, source_repo_path, "cloned")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        cloned_repo_path = os.path.join(repo.cwd(), "cloned")
        assert os.path.isdir(cloned_repo_path)

        # Verify it's a Git repository.
        assert os.path.isdir(os.path.join(cloned_repo_path, ".git"))

    def test_clone_with_depth_option(self, repo, bin):
        """Test cloning with --depth option."""

        # Create a source repository.
        source_repo_path = os.path.join(repo.cwd(), "source")
        os.makedirs(source_repo_path)
        os.chdir(source_repo_path)
        repo.git.init(source_repo_path)
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create multiple commits in the source repository.
        for i in range(3):
            repo.write(f"file{i}.txt", f"content{i}")
            repo.git.add(f"file{i}.txt")
            repo.git.commit("-m", f"Commit {i}")

        # Return to the original working directory.
        os.chdir(repo.cwd())

        # Clone with depth 1.
        result = repo.run(bin, "--depth", "1", source_repo_path, "shallow")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        cloned_repo_path = os.path.join(repo.cwd(), "shallow")
        assert os.path.isdir(cloned_repo_path)

    def test_clone_with_single_branch_option(self, repo, bin):
        """Test cloning with --single-branch option."""

        # Create a source repository.
        source_repo_path = os.path.join(repo.cwd(), "source")
        os.makedirs(source_repo_path)
        os.chdir(source_repo_path)
        repo.git.init(source_repo_path)
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create an initial commit in the source repository.
        repo.write("file.txt", "content")
        repo.git.add("file.txt")
        repo.git.commit("-m", "Initial commit")

        # Return to the original working directory.
        os.chdir(repo.cwd())

        # Clone with single-branch option.
        result = repo.run(
            bin, "--single-branch", source_repo_path, "single-branch-clone"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        cloned_repo_path = os.path.join(repo.cwd(), "single-branch-clone")
        assert os.path.isdir(cloned_repo_path)

    def test_clone_with_multiple_options(self, repo, bin):
        """Test cloning with multiple options forwarded."""

        # Create a source repository.
        source_repo_path = os.path.join(repo.cwd(), "source")
        os.makedirs(source_repo_path)
        os.chdir(source_repo_path)
        repo.git.init(source_repo_path)
        repo.git.config("--local", "user.name", "Test User")
        repo.git.config("--local", "user.email", "test@example.com")

        # Create multiple commits in the source repository.
        for i in range(5):
            repo.write(f"file{i}.txt", f"content{i}")
            repo.git.add(f"file{i}.txt")
            repo.git.commit("-m", f"Commit {i}")

        # Return to the original working directory.
        os.chdir(repo.cwd())

        # Clone with multiple options: --depth and --no-tags.
        result = repo.run(
            bin, "--depth", "2", "--no-tags", source_repo_path, "multi-option"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        cloned_repo_path = os.path.join(repo.cwd(), "multi-option")
        assert os.path.isdir(cloned_repo_path)

    def test_clone_without_arguments(self, repo, bin):
        """Test that git-cl without arguments fails appropriately."""

        result = repo.run(bin)

        # Verify error exit code - 'git clone' will fail without arguments.
        assert result.returncode != 0

    def test_clone_with_invalid_repository(self, repo, bin):
        """Test cloning an invalid repository URL."""

        result = repo.run(bin, "nonexistent-repo")

        # Verify error exit code.
        assert result.returncode != 0
