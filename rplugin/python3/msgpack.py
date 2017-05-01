import neovim
import msgpack
try:
    import ujson as json
except ImportError:
    import json

def strip_whitespace(buffer) -> list:
    return [fmt_line for fmt_line in [line.strip() for line in buffer] if fmt_line != '']

@neovim.plugin
class MsgPackPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.autocmd("BufRead", pattern='*.mp', sync=True, eval='expand("<afile>")')
    def reader(self, filename):
        buffer = self.nvim.current.buffer
        with open(filename, 'rb') as file:
            data = msgpack.loads(file.read(), encoding='utf-8')
        buffer[:] = json.dumps(data, sort_keys=True, indent=4).split('\n')
        buffer.options['modified'] = False

    @neovim.autocmd("BufWriteCmd", pattern='*.mp', sync=True, eval='expand("<afile>")')
    def writer(self, filename) -> None:
        buffer = self.nvim.current.buffer
        data = json.loads('\n'.join(strip_whitespace(buffer)))
        with open(filename, 'wb') as file:
            msgpack.dump(data, file, encoding='utf-8')
        buffer.options['modified'] = False
