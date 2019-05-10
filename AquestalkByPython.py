from ctypes import cdll
import ctypes

dll=cdll.LoadLibrary('./AquesTalk2.dll')

dll.AquesTalk2_Synthe()