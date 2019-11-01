import json
import os


class DestinationFlowBase:
    @classmethod
    def move_to_destination(cls, response, destination):
        raise NotImplementedError


class FileDestinationFlow(DestinationFlowBase):
    @classmethod
    def move_to_destination(cls, response, destination):
        # wrote to separate files in the destination folder
        for key, value in response.items():
            filename = '{}.json'.format(key)
            full_path = os.path.join(destination, filename)
            with open(full_path, 'w') as f:
                json.dump(list(value), f, indent=4)


class MongoDestinationFlow(DestinationFlowBase):
    pass
