"""
Test suite for git-cl command.
"""


class TestGitCl:
    """Test cases for git-cl command."""

    def test_clone_with_repository_url(self, repo, bin):
        """Test cloning a repository with a URL."""

        # Create a bare repository to clone from.
        source_repo_path = repo.path("source.git")
        repo.git.init("--bare", source_repo_path)

        # Clone the repository.
        result = repo.run(bin, source_repo_path, "cloned")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        assert repo.isdir("cloned")

        # Verify it's a Git repository.
        assert repo.isdir("cloned/.git")

    def test_clone_with_depth_option(self, repo, bin):
        """Test cloning with --depth option."""

        # Create a source repository.
        source_repo_path = repo.path("source")
        from git import Repo as GitRepo

        source_git = GitRepo.init(source_repo_path)
        source_git.config_writer().set_value("user", "name", "Test User").release()
        source_git.config_writer().set_value(
            "user", "email", "test@example.com"
        ).release()

        # Create multiple commits in the source repository.
        for i in range(3):
            repo.write(f"source/file{i}.txt", f"content{i}")
            source_git.index.add([f"file{i}.txt"])
            source_git.index.commit(f"Commit {i}")

        # Clone with depth 1.
        result = repo.run(bin, "--depth", "1", source_repo_path, "shallow")

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        assert repo.isdir("shallow")

    def test_clone_with_single_branch_option(self, repo, bin):
        """Test cloning with --single-branch option."""

        # Create a source repository.
        source_repo_path = repo.path("source")
        from git import Repo as GitRepo

        source_git = GitRepo.init(source_repo_path)
        source_git.config_writer().set_value("user", "name", "Test User").release()
        source_git.config_writer().set_value(
            "user", "email", "test@example.com"
        ).release()

        # Create an initial commit in the source repository.
        repo.write("source/file.txt", "Content")
        source_git.index.add(["file.txt"])
        source_git.index.commit("Initial commit")

        # Clone with single-branch option.
        result = repo.run(
            bin, "--single-branch", source_repo_path, "single-branch-clone"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        assert repo.isdir("single-branch-clone")

    def test_clone_with_multiple_options(self, repo, bin):
        """Test cloning with multiple options forwarded."""

        # Create a source repository.
        source_repo_path = repo.path("source")
        from git import Repo as GitRepo

        source_git = GitRepo.init(source_repo_path)
        source_git.config_writer().set_value("user", "name", "Test User").release()
        source_git.config_writer().set_value(
            "user", "email", "test@example.com"
        ).release()

        # Create multiple commits in the source repository.
        for i in range(5):
            repo.write(f"source/file{i}.txt", f"content{i}")
            source_git.index.add([f"file{i}.txt"])
            source_git.index.commit(f"Commit {i}")

        # Clone with multiple options: --depth and --no-tags.
        result = repo.run(
            bin, "--depth", "2", "--no-tags", source_repo_path, "multi-option"
        )

        # Verify success exit code.
        assert result.returncode == 0

        # Verify the cloned repository exists.
        assert repo.isdir("multi-option")

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
