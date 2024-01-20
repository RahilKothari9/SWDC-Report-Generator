import pandas as pd


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

if __name__ == '__main__':
    print(classes_xlsx_to_dict("Classes.xlsx"))