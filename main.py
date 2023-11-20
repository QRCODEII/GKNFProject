from tkinter import messagebox as msg

flag = __name__ == '__main__'
illegal = ['"', '\\', ':']
if flag:
    from tkinter import Tk, Button, Entry
    Y_offset = 0


    def window_center(window: Tk, x=250, y=90):
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
        center_x = int((width-x)/2)
        center_y = int((height-y)/2)
        window.geometry(f'{x}x{y}+{center_x}+{center_y+Y_offset}')


    wd = Tk(className='Main')
    window_center(wd)
else:
    wd = None
words = {}
rev_words = {}
rev_words_txt = ''
try:
    words_txt = open('words.txt', encoding='gbk').read()
    exec('global words\nwords = {'+words_txt+'}')
    txt = words_txt.split('\n')
    for i in range(len(txt)):
        t = txt[i][:-1].split(':')
        rev_words_txt += f'{t[1]}:{t[0]},'
    exec('global rev_words\nrev_words = {' + rev_words_txt + '}')
except FileNotFoundError:
    words_txt = ''
    txt = []
i = 0
while i < len(txt):
    if txt[i] == '':
        txt.pop(i)
        i -= 1
    i += 1


def func_default(func):

    def wrapper(*args, **kwargs):
        if flag:
            global Y_offset
            Y_offset = 120
        return func(*args, **kwargs)

    return wrapper


@func_default
def add(w=None, m=None):
    if flag:
        add_w = Tk(className='AddWords')
        window_center(add_w)
        word = Entry(add_w)
        word.pack()
        meaning = Entry(add_w)
        meaning.pack()
    else:
        add_w = None

    def add_words():
        if flag:
            _w, _m = word.get(), meaning.get()
        else:
            _w, _m = w, m
        if _w == '' or _m == '':
            msg.showerror('Error', '不应为空')
        elif _w in words.keys():
            msg.showerror('Error', '已有此词')
        elif any(n in _w + _m for n in illegal):
            msg.showerror('Error', '包含非法字符')
        else:
            words[_w] = _m
            rev_words[_m] = _w
            txt.append(f'"{_w}":"{_m}",')
            if flag:
                add_w.destroy()

    if flag:
        Button(add_w, text='添加', command=add_words).pack()
        add_w.mainloop()
    else:
        add_words()


@func_default
def modify(w=None, m=None):
    if flag:
        modify_w = Tk(className='ModifyWords')
        window_center(modify_w)
        word = Entry(modify_w)
        word.pack()
        meaning = Entry(modify_w)
        meaning.pack()
    else:
        modify_w = None

    def modify_words():
        if flag:
            _w, _m = word.get(), meaning.get()
        else:
            _w, _m = w, m
        if _w == '':
            msg.showerror('Error', '词不应为空')
        elif _w not in words.keys():
            msg.showerror('Error', '无此词')
        elif _m == '':
            if flag:
                meaning.delete(0, 'end')
                meaning.insert(0, words[_w])
            ask = msg.askyesno('Ask', '是否要删除此词？') if flag else True
            if ask:
                a = 0
                while a < len(txt):
                    if txt[a].split(':')[0] == f'"{_w}"':
                        txt.pop(a)
                        rev_words.pop(words[_w])
                        words.pop(_w)
                        a -= 1
                    a += 1
                if flag:
                    modify_w.destroy()
        elif any(n in _m for n in illegal):
            msg.showerror('Error', '包含非法字符')
        else:
            rev_words.pop(words[_w])
            rev_words[_m] = _w
            words[_w] = _m
            for a in range(len(txt)):
                if txt[a].split(':')[0] == f'"{_w}"':
                    txt[a] = f'"{_w}":"{_m}",'
            if flag:
                modify_w.destroy()

    if flag:
        Button(modify_w, text='修改', command=modify_words).pack()
        modify_w.mainloop()
    else:
        modify_words()


@func_default
def find(w=None):
    if flag:
        find_w = Tk(className='FindWords')
        window_center(find_w)
        word = Entry(find_w)
        word.pack()
        meaning = Entry(find_w, state='readonly')
        meaning.pack()
    else:
        find_w = None

    def find_words():
        _w = word.get() if flag else w
        if _w == '':
            msg.showerror('Error', '不应为空')
        elif _w not in words.keys():
            lst = []
            _flag = False
            for a in rev_words.keys():
                if _w in a:
                    lst.append(a)
                    _flag = True
            if _flag:
                for a in lst:
                    if msg.askyesno('Meanings', f'你是否要找:\n"{rev_words[a]}":"{a}"'):
                        if flag:
                            word.delete(0, 'end')
                            word.insert(0, rev_words[a])
                            meaning.config(state='normal')
                            meaning.delete(0, 'end')
                            meaning.insert(0, a)
                            meaning.config(state='readonly')
                        else:
                            return rev_words[a]
                        break
                else:
                    msg.showerror('Error', '无此词')
            else:
                msg.showerror('Error', '无此词')
        else:
            if flag:
                meaning.config(state='normal')
                meaning.delete(0, 'end')
                meaning.insert(0, words[_w])
                meaning.config(state='readonly')
            else:
                return words[_w]

    if flag:
        Button(find_w, text='查找', command=find_words).pack()
        find_w.mainloop()
    else:
        return find_words()


if flag:
    Button(wd, text='增加词汇', command=add).pack()
    Button(wd, text='修改词汇', command=modify).pack()
    Button(wd, text='查找词汇', command=find).pack()
    wd.mainloop()

file = ''
for i in txt:
    file += i+'\n'
open('words.txt', 'w', encoding='gbk').write(file[:-1])
