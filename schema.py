# Usage: schema = Schema(name).add(name, type, default, required).add(...).compose()
# Usage: schema.empty() -> returns a dict with the schema's default values
# Usage: schema.validate(data) -> returns True if data is valid, False if not


class Schema:
    __composed: bool = False

    def __init__(self, name):
        self.name = name
        self.fields = []

    def add(self, name, type, required: bool = False, default: any = None):
        if self.__composed:
            raise Exception("Schema already composed")
        
        self.fields.append(
            {"name": name, "type": type, "required": required, "default": default}
        )
        return self
    
    def new(self, data: dict):
        # Create a new dict that'll check the data in the passed dict
        # If the data is not in the passed dict, it'll use the default value unless it's required
        new_data = {}

        # Loop through the fields
        for field in self.fields:
            # Check if the field is required
            if field['required'] and field['name'] not in data:
                raise Exception(f"Field {field['name']} is required")
            
            # Check if the field is a Schema
            if isinstance(field["type"], Schema):
                # Check if the field is a dict
                if not isinstance(data[field["name"]], dict):
                    raise Exception(f"Field {field['name']} is not a dict")
                
                # Create a new dict
                new_data[field["name"]] = field["type"].new(data[field["name"]])
                
                # Continue to the next field
                continue

            # Check if the field is the correct type
            if not isinstance(data[field["name"]], field["type"]):
                raise Exception(f"Field {field['name']} is not a {field['type']}")
            
            # Add the field to the new dict
            new_data[field["name"]] = data[field["name"]]
        
        # Return the new dict
        return new_data


    def validate(self, data):
        for field in self.fields:
            # Check if the field is required
            if field['required'] and field['name'] not in data:
                return False
            
            # Check if the field is a Schema
            if isinstance(field["type"], Schema):
                # Check if the field is a dict
                if not isinstance(data[field["name"]], dict):
                    return False
                
                # Validate the field
                if not field["type"].validate(data[field["name"]]):
                    return False
                
                # Continue to the next field
                continue

            # Check if the field is the correct type
            if not isinstance(data[field["name"]], field["type"]):
                return False
            
        return True
    
    def compose(self):
        self.__composed = True
        return self

# Testing if __name__
if __name__ == '__main__':
    # Create a new schema
    schema = Schema(name="User") \
        .add("UserID", int, True, False) \
        .add("Economy", Schema(name="Economy") \
            .add("Balance", int, True, 0) \
            .add("Bank", int, True, 0) \
            .add("LastDaily", int, True, 0) \
            .compose(), True, {}) \
        .compose()

    # Print the schema
    print(schema.new())

    # Create a new user
    user = schema.new()
    user["UserID"] = 1234567890
    user["Economy"]["Balance"] = 1000

    # Validate the user
    print(schema.validate(user))