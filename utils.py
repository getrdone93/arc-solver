from matplotlib import colors, pyplot
import numpy as np
import priors

BLACK = 'k'
BLUE = 'b'
RED = 'r'
GREEN = 'g'
YELLOW = 'y'
GRAY = '0.75'
PINK = '#FF69B4'
ORANGE = '#FFA500'
CYAN = '#00FFFF'
MAROON = '#800000'

def display(grid):
    np_g = np.array(grid)
    r, c = np_g.shape[0], np_g.shape[1]
    cmap = colors.ListedColormap([BLACK, BLUE, RED, GREEN, YELLOW, GRAY, 
                                  PINK, ORANGE, CYAN, MAROON])
    bounds = range(10)
    np_bs = np.array(bounds)
    norm = colors.BoundaryNorm(bounds, cmap.N - 1)
    fig, ax = pyplot.subplots()
    ax.matshow(np_g, cmap=cmap, norm=norm)
    ax.grid(linewidth=2, color='0.5')
    ax.set_xticks(np.arange(-.5, c, 1))
    ax.set_yticks(np.arange(-.5, r, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    pyplot.show()

def test_data(width, height, num_objs, background=0):
    data = np.random.randint(0, 10, width*height).reshape((width, height)) if background == 1 \
           else np.zeros((width, height))
    colors = np.random.choice(10, num_objs, replace=False)

    for c in colors:
        sr = np.random.randint(1, height // 2)
        er = np.random.randint(height // 2 + 1, height)
        sc = np.random.randint(1, width // 2)
        ec = np.random.randint(width // 2 + 1, width)
        data[sr:er, sc:ec] = c

    return data

def object_cohesion_lists(inputs, outputs):
    return [[priors.object_cohesion(i) for i in ds] for ds in (inputs, outputs)]

def num_objs(inp_coh, out_coh):
    return [[priors.num_objs(oc) for oc in ds] for ds in (inp_coh, out_coh)]

def pixel_count(inp_coh, out_coh):
    return [[priors.pixel_count(oc) for oc in ds] for ds in (inp_coh, out_coh)]

def pixel_count_desc(inp_coh, out_coh):
    return [[priors.pixel_count_desc(oc) for oc in ds] for ds in (inp_coh, out_coh)]

def smallest_enclosing_img(obj: tuple):
    rs, cs = obj
    return np.zeros(((max(rs) - min(rs)) + 1, (max(cs) - min(cs)) + 1), dtype=np.uint8)

def func_reduce(funcs, iv):
    if len(funcs) <= 0:
        return iv
    return func_reduce(funcs[1:], funcs[0](iv))

def single_object_outputs(cohs):
    _, o = num_objs(cohs, cohs)
    return set(o) == {1}

def get_dims(image: list):
    return np.asarray(image).shape

def image_list_shapes(image_list):
    return [get_dims(i) for i in image_list]

def pairwise_equal(inputs, outputs):
    ins, outs = [np.asarray(image_list_shapes(ds)) for ds in (inputs, outputs)]
    return ins, outs, np.all(ins == outs)

def func_on_iters_va(func, *iterables):
    return [[func(*e) for e in it] for it in iterables]

def func_on_iters(func, *iterables):
    return [[func(e) for e in it] for it in iterables]

def func_on_iters_mapf(func, map_func, *iterables):
    return [[func(*map_func(e)) for e in it] for it in iterables]

