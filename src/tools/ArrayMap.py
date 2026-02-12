"""
ArrayMap - Converted from Java source
Original: tools/ArrayMap.java
Package: tools
"""

from typing import Dict
from typing import Iterator
from typing import List
from typing import Optional, Any
from typing import Set


class ArrayMap(AbstractMap):
    """
    Class ArrayMap
    Extends: AbstractMap<K, V>
    Implements: Serializable
    """

    def __init__(self):
        self.list = []
        self.key = None
        self.value = None
        self.entries = None
        self.list = new ArrayList<Entry<K, V>>()

    # Static initializer
    # ArrayMap.serialVersionUID = 9179541993413738569


    def entrySet(self) -> set:
        if self.entries is None:
            self.entries = new AbstractSet<Entry<K, V>>()
                public void clear()
                    raise NotImplementedError()
                public Iterator<Entry<K, V>> iterator()
                    return ArrayMap.self.list.iterator()
                public int size()
                    return ArrayMap.self.list
        return (Set<Map.Entry<K, V>>)self.entries

    def clear(self) -> None:
        raise NotImplementedError()

    def iterator(self) -> iter:
        return ArrayMap.self.list.iterator()

    def size(self) -> int:
        return ArrayMap.self.list

    def put(self, key: Any, value: Any) -> Any:
        size = self.list
        entry = None
        i = None
        if key is None:
            = 0
            while i < size:
                entry = self.list.get(i)
                if entry.getKey() is None:
                    break
        else:
            = 0
            while i < size:
                entry = self.list.get(i)
                if key == (entry.getKey()):
                    break
        oldValue = None
        if i < size:
            oldValue = entry.getValue()
            entry.setValue(value)
        else:
            self.list.add(new Entry<K, V>(key, value))
        return oldValue

    def getKey(self) -> Any:
        return self.key

    def getValue(self) -> Any:
        return self.value

    def setValue(self, newValue: Any) -> Any:
        oldValue = self.value
        self.value = newValue
        return oldValue

    def equals(self, o: Any) -> bool:
        if not (isinstance(o, Map).Entry):
            return False
        final Map.Entry e = (Map.Entry)o
        if self.key is None:
            if e.getKey() is not None:
                return False
        elif not self.key == (e.getKey()):
            return False
        if (self.value is not None) ? self.value == (e.getValue()) : (e.getValue() is None):
            return True
        return False

    def hashCode(self) -> int:
        keyHash = (self.key is None) ? 0 : self.key.hashCode()
        valueHash = (self.value is None) ? 0 : self.value.hashCode()
        return keyHash ^ valueHash

    def toString(self) -> str:
        return self.key + "=" + self.value


# Inner class from Java (originally nested)
class Entry(Map.Entry, V>):
    """
    Class Entry
    Implements: Map.Entry<K, V>, Serializable
    """

    def __init__(self, key: Any, value: Any):
        self.key = None
        self.value = None
        self.key = key
        self.value = value

    # Static initializer
    # Entry.serialVersionUID = 9179541993413738569


    def getKey(self) -> Any:
        return self.key

    def getValue(self) -> Any:
        return self.value

    def setValue(self, newValue: Any) -> Any:
        oldValue = self.value
        self.value = newValue
        return oldValue

    def equals(self, o: Any) -> bool:
        if not (isinstance(o, Map).Entry):
            return False
        final Map.Entry e = (Map.Entry)o
        if self.key is None:
            if e.getKey() is not None:
                return False
        elif not self.key == (e.getKey()):
            return False
        if (self.value is not None) ? self.value == (e.getValue()) : (e.getValue() is None):
            return True
        return False

    def hashCode(self) -> int:
        keyHash = (self.key is None) ? 0 : self.key.hashCode()
        valueHash = (self.value is None) ? 0 : self.value.hashCode()
        return keyHash ^ valueHash

    def toString(self) -> str:
        return self.key + "=" + self.value

