import argparse
import sys
import json
import re

states={"cur_room":None,"inventory":[]}
user_input=None
commands = {
    "go": "go ...",
    "get": "get ...",
    "look": "look",
    "inventory": "inventory",
    "quit": "quit",
    "help": "help"
}
def main():
    parser=argparse.ArgumentParser(prog=adventure)
    parser.add_argument("map_filename")
    args=parser.parse_args()
    if(args.map_filename):
        try:
            with open(f"../assets/{args.map_filename}") as file:
                loop_map=json.loads(file.read())
                adventure(loop_map)
        except ValueError:
            raise ValueError("should be value file name")


def adventure(loop_map):
    states.update({"cur_room":0})
    while(True):
        current_room=loop_map[states.get("cur_room")]
        room_info = f"> {current_room.get('name')}\n\n{current_room.get('desc')}\n\n"
        if 'items' in current_room and current_room['items']:
            room_info += "Items: " + ", ".join(current_room['items']) + "\n\n"
        exits = "Exits: " + " ".join(current_room.get('exits').keys()) + "\n"
        user_input = input(room_info + exits + "\nWhat would you like to do? ")
        if("quit" in user_input):
            print("Goodbye!")
            break
        if user_input.lower() == "help":
            display_help()
            continue
        if("look" in user_input):
            user_input=input(f"> {current_room.get('name')}\n\n{current_room.get('desc')}\n\n{exits}\n\nWhat would you like to do? ")
        arg=parser(user_input,current_room)
        res=implementation(arg,current_room)
        if("quit" in res):
            print("Goodbye")
            break
        while("noitem" in res or "inventory" in res or "getitem" in res or "nodir" in res):
            user_input=res[1]
            arg=parser(user_input,current_room)
            res=implementation(arg,current_room)

def display_help():
    print("You can run the following commands:")
    for command, description in commands.items():
        print(f"  {description}")
    print()
    
def parser(user_input,cur_room):
    directions=["east","south","west","north"]
    user_input=user_input.lower()
    if(not user_input):
        return ("nodir")
    if("^" in user_input):
        print("Use 'quit' to exit.")
        return ("EOF")
    if "go" in user_input:
        pattern=r"(east|west|north|south)"
        match=re.findall(pattern,user_input)
        while(len(match)==0 or len(match)>2):
            if("quit" in user_input):
                return("quit")
            return ("nodir")
        suc_room=cur_room.get("exits").get(match[0])
        if(not suc_room):
            return ("wrongdir",match[0])
        print(f"You go {match[0]}. ")
        return ("go",suc_room)
    elif "get" in user_input:
        reg=r"(get\s)(\w+)";
        match=re.findall(reg,user_input);
        item=match[0][1]
        return ("get",item)
    elif "inventory" in user_input:
        return ("inventory")
    else:
        return ("unknown verb")



def implementation(arg,cur_room):
    if(arg=="quit"):
        return ("quit")
    if(arg=="unknown verb"):
        user_input=input("Cannot recognize the argument. \nWhat would you like to do? ")
        return ("unkown")
    if("go" in arg):
        states.update({"cur_room":arg[1]})
        return ("updatego")
    if("nodir" in arg):
        user_input=input("Sorry, you need to 'go' somewhere.\nWhat would you like to do? ")
        return ("nodir",user_input)
    if("wrongdir" in arg):
        user_input=input(f"There is no way to go {arg[1]}. \nWhat would you like to do? ")
        return ("nodir",user_input)
    if("get" in arg):
        items=cur_room.get("items")
        new_item=arg[1]
        if not items or new_item not in items:
            print(f"There's no {new_item} anywhere.")
            user_input=input("What would you like to do? ")
            return ("noitem",user_input)
        else:
            items.remove(new_item)
            states.get("inventory").append(new_item)
            print(f"You pick up the {new_item}")
            user_input=input("What would you like to do? ")
            return("getitem",user_input)
    if("inventory" in arg):
        print(f"Inventory: \n  {', '.join(states.get('inventory'))}")
        user_input=input("What would you like to do? ")
        return ("inventory",user_input)
            
if __name__=="__main__":
    main()

