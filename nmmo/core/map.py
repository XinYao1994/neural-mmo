from pdb import set_trace as T
import numpy as np

from nmmo import core
from nmmo.core import terrain
from nmmo.lib import material

import os

class Map:
   '''Map object representing a list of tiles
   
   Also tracks a sparse list of tile updates
   '''
   def __init__(self, config, realm):
      self.config = config

      sz          = config.TERRAIN_SIZE
      self.tiles  = np.zeros((sz, sz), dtype=object)

      for r in range(sz):
         for c in range(sz):
            self.tiles[r, c] = core.Tile(config, realm, r, c)

   @property
   def packet(self):
       '''Packet of degenerate resource states'''
       missingResources = []
       for e in self.updateList:
           missingResources.append(e.pos)
       return missingResources

   @property
   def repr(self):
      '''Flat matrix of tile material indices'''
      return [[t.mat.index for t in row] for row in self.tiles]

   def reset(self, realm, idx):
      '''Reuse the current tile objects to load a new map'''

      path_maps = os.path.join(self.config.PATH_CWD, self.config.PATH_MAPS)
      os.makedirs(path_maps, exist_ok=True)
      if not os.listdir(path_maps):
         terrain.MapGenerator(self.config).generate()

      self.updateList = set()
      materials = {mat.index: mat for mat in material.All}

      path_map_suffix = self.config.PATH_MAP_SUFFIX.format(idx)
      fPath  = os.path.join(path_maps, path_map_suffix)
      for r, row in enumerate(np.load(fPath)):
         for c, idx in enumerate(row):
            mat  = materials[idx]
            tile = self.tiles[r, c]
            tile.reset(mat, self.config)

   def step(self):
      '''Evaluate updatable tiles'''
      for e in self.updateList.copy():
         if e.static:
            self.updateList.remove(e)
         e.step()

   def harvest(self, r, c):
      '''Called by actions that harvest a resource tile'''
      self.updateList.add(self.tiles[r, c])
      return self.tiles[r, c].harvest()