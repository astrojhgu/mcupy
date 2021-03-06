def log_progress(sequence, every=None, size=None):
	from ipywidgets import IntProgress, HTML, VBox
	from IPython.display import display

	is_iterator = False
	if size is None:
		try:
			size = len(sequence)
		except TypeError:
			is_iterator = True
	if size is not None:
		if every is None:
			if size <= 200:
				every = 1
			else:
				every = size / 200     # every 0.5%
	else:
		assert every is not None, 'sequence is iterator, set every'

	if is_iterator:
		progress = IntProgress(min=0, max=1, value=1)
		progress.bar_style = 'info'
	else:
		progress = IntProgress(min=0, max=size, value=0)
	label = HTML()
	box = VBox(children=[label, progress])
	display(box)

	index = 0
	try:
		for index, record in enumerate(sequence, 1):
			if index == 1 or index % every == 0:
				if is_iterator:
					label.value = '{index} / ?'.format(index=index)
				else:
					progress.value = index
					label.value = u'{index} / {size}'.format(
						index=index,
						size=size
				)
			yield record
	except:
		progress.bar_style = 'danger'
		raise
	else:
		progress.bar_style = 'success'
		progress.value = index
		label.value = str(index or '?')


def display_graph(g):
	from IPython.display import Image, display
	try:
		import pydot_ng as pydot
	except(ImportError):
		import pydot
	t=g.dumpTopology()
	dot=pydot.Dot()
	for i in t:
		dot.add_edge(pydot.Edge(pydot.Node(i[1]),pydot.Node(i[0])))
	plt = Image(dot.create_png())
	display(plt)
	
