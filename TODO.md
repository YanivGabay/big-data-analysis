## todo

- [X] Create a `requirements.txt` file with the necessary dependencies.
- [X] Create a `main.py` file that will be the entry point of the application.
- [X] Create a `modules` directory with the following modules:
  - [X] `loader.py`: responsible for loading the data.
  - [X] `processor.py`: responsible for processing the data.
  - [X] `analyzer.py`: responsible for analyzing the data.

- [X] `/pages`: All pages have a:
  
```python
def show():
    setup_something()
    something()

```

  i think it will be good to move this logic to a outside class maybe, to avoid code duplication,
  aswell allowing to different pages to have different setups using the same method/instance/class/what is needed.

- [X] Create some variable to control the logger output, like a debug variable, to avoid print all the time.

- [ ] UML diagram of the project.

- [ ] Add some easy spinner/loader module to all the pages, not only loader.py.
  
