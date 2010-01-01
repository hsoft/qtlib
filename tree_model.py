# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-09-14
# $Id$
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "BSD" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/bsd_license

from PyQt4.QtCore import Qt, QAbstractItemModel, QModelIndex

class NodeContainer(object):
    def __init__(self):
        self._subnodes = None
        self._ref2node = {}
    
    #--- Protected
    def _createNode(self, ref, row):
        # This returns a TreeNode instance from ref
        raise NotImplementedError()
    
    def _getChildren(self):
        # This returns a list of ref instances, not TreeNode instances
        raise NotImplementedError()
    
    #--- Public
    def invalidate(self):
        # Invalidates cached data and list of subnodes without resetting ref2node.
        self._subnodes = None
    
    #--- Properties
    @property
    def subnodes(self):
        if self._subnodes is None:
            children = self._getChildren()
            self._subnodes = []
            for index, child in enumerate(children):
                if child in self._ref2node:
                    node = self._ref2node[child]
                    node.row = index
                else:
                    node = self._createNode(child, index)
                    self._ref2node[child] = node
                self._subnodes.append(node)
        return self._subnodes
    

class TreeNode(NodeContainer):
    def __init__(self, model, parent, row):
        NodeContainer.__init__(self)
        self.model = model
        self.parent = parent
        self.row = row
    
    @property
    def index(self):
        return self.model.createIndex(self.row, 0, self)
    

class TreeModel(QAbstractItemModel, NodeContainer):
    def __init__(self):
        QAbstractItemModel.__init__(self)
        NodeContainer.__init__(self)
        self._dummyNodes = set() # dummy nodes' reference have to be kept to avoid segfault
    
    #--- Private
    def _createDummyNode(self, parent, row):
        # In some cases (drag & drop row removal, to be precise), there's a temporary discrepancy
        # between a node's subnodes and what the model think it has. This leads to invalid indexes
        # being queried. Rather than going through complicated row removal crap, it's simpler to
        # just have rows with empty data replacing removed rows for the millisecond that the drag &
        # drop lasts. Override this to return a node of the correct type.
        return TreeNode(self, parent, row)
    
    #--- Overrides
    def index(self, row, column, parent):
        if not self.subnodes:
            return QModelIndex()
        node = parent.internalPointer() if parent.isValid() else self
        try:
            return self.createIndex(row, column, node.subnodes[row])
        except IndexError:
            parentNode = parent.internalPointer() if parent.isValid() else None
            dummy = self._createDummyNode(parentNode, row)
            self._dummyNodes.add(dummy)
            return self.createIndex(row, column, dummy)
    
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        node = index.internalPointer()
        if node.parent is None:
            return QModelIndex()
        else:
            return self.createIndex(node.parent.row, 0, node.parent)
    
    def reset(self):
        self.invalidate()
        self._ref2node = {}
        self._dummyNodes = set()
        QAbstractItemModel.reset(self)
    
    def rowCount(self, parent):
        node = parent.internalPointer() if parent.isValid() else self
        return len(node.subnodes)
    
    #--- Public
    def findIndex(self, rowPath):
        """Returns the QModelIndex at `rowPath`
        
        `rowPath` is a sequence of node rows. For example, [1, 2, 1] is the 2nd child of the
        3rd child of the 2nd child of the root.
        """
        result = QModelIndex()
        for row in rowPath:
            result = self.index(row, 0, result)
        return result
    
    @staticmethod
    def pathForIndex(index):
        reversedPath = []
        while index.isValid():
            reversedPath.append(index.row())
            index = index.parent()
        return list(reversed(reversedPath))
    
