import unittest
import docker

class TestDocker(unittest.TestCase):
    def setUp(self):
        self.client = docker.from_env()

    def test_docker_container_runs(self):
        # Build the Docker image
        self.client.images.build(path=".")

        # Run the Docker container
        container = self.client.containers.run("streamlit_app", detach=True)

        # Check that the container is running
        try:
            self.assertTrue(container.status == "running")
        except AssertionError:
            print(container.logs().decode('utf-8'))
            raise

        # Stop and remove the container
        container.stop()
        container.remove()

if __name__ == '__main__':
    unittest.main()