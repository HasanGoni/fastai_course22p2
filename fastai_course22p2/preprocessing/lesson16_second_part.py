"""Reproducing lesson 16 part2"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/04_preprocessing.lesson_16_second_part.ipynb.

# %% auto 0
__all__ = ['dsd', 'set_seed', 'prep_data', 'conv', 'conv_layers', 'fit', 'SequentialModel', 'append_stats', 'Hook', 'Hooks',
           'get_hist', 'get_min']

# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 3
from cv_tools.core import *


# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 4
import matplotlib as mpl
import logging
import random
import numpy as np
import matplotlib.pyplot as plt
from functools import partial
from fastcore.all import *
logging.disable(logging.WARNING)

# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 5
from datasets import load_dataset

# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 6
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms.functional as TF
from torcheval.metrics import MulticlassAccuracy

# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 8
def set_seed(seed, deterministic=False):
    torch.use_deterministic_algorithms(deterministic)
    torch.manual_seed(seed)
    random.seed(seed)
    np.random.seed(seed)

# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 12
dsd = load_dataset('fashion_mnist')
def prep_data():
	tds = dsd.with_transform(transformi)
	dls = DataLoaders.from_dd(tds, batch_size=1024, num_workers=4)
	return dls


# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 14
def conv(ni, nf, ks=3, act=True):
	res = nn.Conv2d(ni, nf, ks, stride=2, padding=ks//2)
	if act: res = nn.Sequential(res, nn.ReLU())
	return res


# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 15
def conv_layers():
	return [
		conv(1, 8, ks=5), # 14x14
		conv(8, 16), # 7x7
		conv(16, 32), # 4x4
		conv(32, 64), # 2x2
		conv(64, 10, act=False), # 1x1
		nn.Flatten()
	]

# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 17
def fit(model, epochs=1):
	learn = Learner(
		model, dls, 
		loss_func=F.cross_entropy, 
		lr=0.6,
		cbs=cbs,
	)
	learn.fit(epochs)
	return learn


# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 21
class SequentialModel(nn.Module):
	def __init__(self, *layers):
		super().__init__()
		self.layers = nn.ModuleList(layers)
		self.act_means = [[] for _ in self.layers]
		self.act_stds = [[] for _ in self.layers]

	def __call__(self, x):
		for i, layer in enumerate(self.layers):
			x = layer(x)
			self.act_means[i].append(to_cpu(x.mean()))
			self.act_stds[i].append(to_cpu(x.std()))
		return x

	def __iter__(self):
		return iter(self.layers)

	def __len__(self):
		return len(self.layers)


# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 27
def append_stats(i, mod, inp, out):
	act_means[i].append(to_cpu(out.mean()))
	act_stds[i].append(to_cpu(out.std()))


# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 31
class Hook():
	def __init__(self, module, func):
		self.hook = module.register_forward_hook(partial(func, self))

	def remove(self):
		self.hook.remove()

	def __del__(self):
		self.remove()


# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 32
def append_stats(h, mod, inp, out):
	if not hasattr(h, 'stats'):h.stats = ([], [])
	act = to_cpu(out)
	h.stats[0].append(act.mean())
	h.stats[1].append(act.std())


# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 37
class Hooks(list):
	# Initialize the Hooks class by creating a list of Hook objects for each module in the input list 'ms'.
	# Each Hook is created with the module 'm' and the function 'append_stats'.
	def __init__(self, ms, f):
		super().__init__([Hook(m, f) for m in ms])
	
	# This method is called when the Hooks object is used as a context manager.
	# It returns the Hooks object itself, allowing it to be used in a 'with' statement.
	def __enter__(self, *args):return self
	# This method is called when the 'with' statement is exited.
	# It calls the 'remove' method to clean up any resources used by the Hooks.
	def __exit__(self, *args):self.remove()
	# This method is called when the Hooks object is about to be garbage collected.
	# It calls the 'remove' method to clean up any resources used by the Hooks.
	def __del__(self):self.remove()
	# This method is called when an item is deleted from the Hooks list.
	# It removes the Hook object at the specified index 'i' and then calls the superclass's __delitem__ method.
	def __delitem__(self, i):
		self[i].remove()
		super().__delitem__(i)
	# This method removes all Hook objects in the Hooks list.
	# It iterates over each Hook in the list and calls its 'remove' method.
	def remove(self):
		for h in self: h.remove()

# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 41
def append_stats(h, mod, inp, out):
	if not hasattr(h, 'stats'):h.stats = ([], [], [])
	act = to_cpu(out)
	h.stats[0].append(act.mean())
	h.stats[1].append(act.std())
	h.stats[2].append(act.histc(40,0, 10))



# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 46
def get_hist(h):return torch.stack(h.stats[2]).t().float().log1p()



# %% ../../nbs/04_preprocessing.lesson_16_second_part.ipynb 52
def get_min(h):
	h1 = torch.stack(h.stats[2]).t().float().log1p()
	return h1[:2].sum(0)/h1.sum(0)

