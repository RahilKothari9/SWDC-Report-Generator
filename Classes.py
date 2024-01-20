import pandas as pd

class Classrooms:
    def __init__(self, building, room, capacity):
        self.building = building
        self.room = room
        self.capacity = capacity

    def __str__(self):
        return f"Classrooms({self.building}, {self.room}, {self.capacity})"

def classes_xlsx_to_dict(path = None):
    if path is None or path == "":
        raise Exception("Path Not Provided")
    try:
        df = pd.read_excel(path, sheet_name=None, header=0, index_col=0)
        buildings = {}
        for sheet in df:
            # make sure the index column is read as string
            df[sheet].index = df[sheet].index.astype(str)
            buildings[sheet] = {}
            st: dict = buildings[sheet]
            
            # Add the capacity of each room to the dictionary
            st.update(df[sheet].to_dict()['Capacity'])
        return buildings
    
    except Exception as e:
        print(e)
        return None
    
def get_classrooms(path: str = None):
    if path is None or path == "":
        raise Exception("Path Not Provided")
    try:
        df = pd.read_excel(path, sheet_name=None, header=0, index_col=0)
        classrooms = []
        for sheet in df:
            # make sure the index column is read as string
            df[sheet].index = df[sheet].index.astype(str)
            for index, row in df[sheet].iterrows():
                classrooms.append(Classrooms(sheet, index, row['Capacity']))
        return classrooms
    
    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    print(classes_xlsx_to_dict("Classes.xlsx"))
    classes = get_classrooms("Classes.xlsx")
    for classroom in classes:
        print(classroom)