import json
import os
from models.posts import Post
classes = {"Post": Post}

class FileStorage:
    """ Store objects in json file """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None) -> dict:
        """ Return all objects """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """ Add object to __objects """
        if obj is not None:
            key = obj.__class__.__name__ + "." + str(obj.id)
            self.__objects[key] = obj

    def save(self):
        """ Serialize __objects to json file """
        new_dict = {}
        for key in self.__objects:
            if key == "password":
                new_dict[key].decode()
            new_dict[key] = self.__objects[key].to_dict(save_fs=True)
        with open(self.__file_path, "w") as file:
            json.dump(new_dict, file)

    def reload(self):
        """ Deserialize json file to __objects """
        try:
            if os.path.exists(self.__file_path):
                with open(self.__file_path, "r") as file:
                    new_dict = json.load(file)
                for key in new_dict:
                    self.__objects[key] = eval(new_dict[key]["__class__"])(**new_dict[key])
        except:
            print("Error loading file")

    def delete(self, obj=None):
        """ Delete object from __objects """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """ Deserialize json file to __objects """
        self.reload()

    def get(self, cls, id):
        """ Get object by id """
        if cls and id:
            if cls in classes.values():
                all_objs = self.all(cls)
                for obj in all_objs.values():
                    if obj.id == id:
                        return obj
        return None

    def count(self, cls=None):
        """ Count objects """
        if cls is not None:
            all_objs = self.all(cls)
            return len(all_objs)
        if cls in classes.values():
            all_objs = self.all(cls)
            return len(all_objs)
        return None

