from PySide6.QtCore import QObject, Signal, QRunnable, Slot

import traceback


class AsyncWorker(QRunnable):
	class Signals(QObject):
		started = Signal()
		finished = Signal(object)
		error = Signal(str)
		progress = Signal(int)
		
	def __init__(self, fn, *args, **kwargs):
		super().__init__()
		
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
		self.signals = self.Signals()
		self.setAutoDelete(True)
		
	@Slot()
	def run(self):
		self.signals.started.emit()
		
		try:
			result = self.fn(*self.args, **self.kwargs)
			self.signals.finished.emit(result)
			
		except Exception as e:
			self.signals.error.emit(f"{e}\n{traceback.format_exc()}")