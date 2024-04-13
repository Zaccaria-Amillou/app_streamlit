import unittest
import docker

class TestDocker(unittest.TestCase):
    def setUp(self):
        self.client = docker.from_env()

    def test_docker_container_runs(self):
        # Build the Docker image
        self.client.images.build(path=".")

        # Run the Docker container
        container = self.client.containers.run("your-image-name", detach=True)

        # Check that the container is running
        self.assertTrue(container.status == "running")

        # Stop and remove the container
        container.stop()
        container.remove()

if __name__ == '__main__':
    unittest.main()