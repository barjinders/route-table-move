import oci
import json
from datetime import datetime


start = datetime.now()
config = oci.config.from_file("~/.oci/configp", "DEFAULT")
# open the JSON file
f = open('userInputs.json')

# parse the JSON file
try:
    data = json.load(f)
except json.decoder.JSONDecodeError:
    print("Invalid documentTemplate JSON")


source_compartment_id = data["source_compartment_id"]
destination_compartment_id = data["destination_compartment_id"]

# Initialize service client with default config file
core_client = oci.core.VirtualNetworkClient(config)


def change_route_table_compartment(core_client, source_compartment_id, dest_compartment_id):
    try:

        list_route_tables_response = core_client.list_route_tables(
            compartment_id=source_compartment_id,
            lifecycle_state="AVAILABLE")
        print(str(len(list_route_tables_response.data))+ " Route tables will be moved from to the destination compartment.")    
        for x in list_route_tables_response.data:
            print("\nMoving the route table " + str(x.display_name) +
                  " to the destination compartment\n")
            change_route_table_compartment_response = core_client.change_route_table_compartment(
                rt_id=x.id,
                change_route_table_compartment_details=oci.core.models.ChangeRouteTableCompartmentDetails(
                    compartment_id=dest_compartment_id))
            print(change_route_table_compartment_response.headers)
    except oci.exceptions.ServiceError as e:
        print(" ERROR: Change Route Table Compartment API call failed:")
        print(e)

change_route_table_compartment(core_client, source_compartment_id, destination_compartment_id)

#calculate the execution time
end = datetime.now()
print("The time of execution of above program is :",
      str(end-start)[5:])