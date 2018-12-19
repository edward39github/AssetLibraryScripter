
class InfoRecord(object):

    RecordTypeInt           = "int"
    RecordTypeBool          = "bool"
    RecordTypeColor         = "color"
    RecordTypeFloat         = "float"
    RecordTypeString        = "string"
    RecordTypeRangeInt      = "range_int"
    RecordTypeRangeFloat    = "range_float"
    RecordTypeResolution    = "resolution"
    RecordTypeListString    = "list_string"
    RecordTypeListFloat     = "list_float"
    RecordTypeListColor     = "list_color"
    RecordTypeListInt       = "list_int"



    def __init__(self, name=""):
        super(InfoRecord, self).__init__()

        if not isinstance(name, str):
            raise TypeError("Expected < str >")

        self._name = name
        self._type = ""
        self._value = ""


    def __eq__(self, other):
        if not isinstance(other, InfoRecord):
            return False

        return self._name == other.name



    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Expected < str >")

        self._name = name


    def toDict(self):
        return {
            "name": self._name,
            "type": self._type,
            "value": self._value
        }


    def setValueBool(self, value=0):
        if not isinstance(value, bool):
            raise TypeError("Expected < bool >")
        self._type = InfoRecord.RecordTypeBool
        self._value = value


    def setValueInt(self, value=0):
        if not isinstance(value, int):
            raise TypeError("Expected < int >")
        self._type = InfoRecord.RecordTypeInt
        self._value = value


    def setValueFloat(self, value=0.0):
        if not isinstance(value, float):
            raise TypeError("Expected < float >")
        self._type = InfoRecord.RecordTypeFloat
        self._value = value


    def setValueString(self, value="abc"):
        if not isinstance(value, str):
            raise TypeError("Expected < str >")
        self._type = InfoRecord.RecordTypeString
        self._value = value


    def setValueColor(self, value="#000000"):
        if not isinstance(value, str):
            raise TypeError("Expected < str >")
        self._type = InfoRecord.RecordTypeColor
        self._value = value


    def setValueResolution(self, value=(1024, 1024)):
        if not isinstance(value, tuple):
            raise TypeError("Expected < tuple(int) >")
        self._type = InfoRecord.RecordTypeResolution
        self._value = value


    def setValueRangeInt(self, value=(-10, 10)):
        if not isinstance(value, tuple):
            raise TypeError("Expected < tuple(int) >")
        self._type = InfoRecord.RecordTypeRangeInt
        self._value = value


    def setValueRangeFloat(self, value=(0.0, 1.0)):
        if not isinstance(value, tuple):
            raise TypeError("Expected < tuple(float) >")
        self._type = InfoRecord.RecordTypeRangeFloat
        self._value = value


    def setValueStringList(self, value=[""]):
        if not isinstance(value, list):
            raise TypeError("Expected < list(str) >")

        self._type = InfoRecord.RecordTypeListString
        self._value = value


    def setValueColorList(self, value=[""]):
        if not isinstance(value, list):
            raise TypeError("Expected < list(color) >")

        self._type = InfoRecord.RecordTypeListColor
        self._value = value


    def setValueFloatList(self, value=[""]):
        if not isinstance(value, list):
            raise TypeError("Expected < list(float) >")

        self._type = InfoRecord.RecordTypeListFloat
        self._value = value


    def setValueIntList(self, value=[""]):
        if not isinstance(value, list):
            raise TypeError("Expected < list(int) >")

        self._type = InfoRecord.RecordTypeListInt
        self._value = value




class InfoRecordGroup(object):

    def __init__(self):
        super(InfoRecordGroup, self).__init__()

        self._name = ""
        self._records = []


    def __getitem__(self, item):
        if isinstance(item, int):
            return self._records[item]

        if isinstance(item, str):
            for record in self._records:
                if record.name == item:
                    return record

            raise KeyError("No record named " + item)

        raise KeyError("Unsupported key type. Expect < int > or < str >")


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Expected < str >")

        self._name = name


    def toDict(self):
        return {
            "group": self._name,
            "records": [record.toDict() for record in self._records]
        }


    def addRecord(self, record, index=None):
        """
        Append record to group. If record already exist return False, otherwise True

        :param record: < InfoRecord >

        :param index: < int > insertion index, if None append

        :return: bool
        """

        if not isinstance(record, InfoRecord):
            return False

        if record in self._records:
            return False

        if index == None:
            self._records.append(record)
            return True

        self._records.insert(index, record)

        return True


    def removeRecord(self, item):
        """
        Remove record by index or record name.

        :param item: index or record name

        :return: bool
        """

        if isinstance(item, int):
            self._records.pop(item)
            return True

        if isinstance(item, str):
            for i, record in enumerate(self._records):
                if record.name == item:
                    self._records.pop(i)
                    return True

            raise KeyError("No record named " + item)

        raise KeyError("Unsupported item type. Expect < int > or < str >")


    def changeRecord(self, name, new_record):
        if not isinstance(name, str):
            raise TypeError("parm name: expected < str >")

        if not isinstance(new_record, InfoRecord):
            raise TypeError("parm new_record: expected < InfoRecord >")

        for i, record in enumerate(self._records):
            if record.name == name:
                if new_record not in self._records:
                    self._records[i] = record
                    return True
        return False


    def makeDefault(self, uniqid, tags, categories, groups, sets, name):
        rec_uniqid = InfoRecord("ID")
        rec_tags = InfoRecord("Tags")
        rec_categories = InfoRecord("Categories")
        rec_groups = InfoRecord("Groups")
        rec_name = InfoRecord("Name")
        rec_set = InfoRecord("Sets")

        rec_uniqid.setValueString(uniqid)
        rec_tags.setValueStringList(tags)
        rec_categories.setValueStringList(categories)
        rec_groups.setValueStringList(groups)
        rec_name.setValueString(name)
        rec_set.setValueStringList(sets)


        self._name = "asset"
        self._records = [
            rec_uniqid,
            rec_tags,
            rec_categories,
            rec_groups,
            rec_set,
            rec_name
        ]
