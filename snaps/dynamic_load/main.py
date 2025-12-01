import settings 
from misc import load_object


def load_pipes():
    pipes = settings.PIPELINES
    sorted_pipes = sorted(pipes.items(), key=lambda kv: kv[1])
    cls_list = []
    for k, _ in sorted_pipes:
        cls = load_object(k)
        cls_list.append(cls())
    return cls_list

def main(data: str):

    pipes = load_pipes()
    for pipe in pipes:
        pipe.process(data=data)


if __name__ == "__main__":
    data="a1min"
    main(data=data)
