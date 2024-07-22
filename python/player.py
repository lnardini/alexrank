class Player():

  def __init__(self, name: str = "", id: str = "", slug: str = "") -> None:
    self.name = name
    self.id = id
    self.slug = slug

  def __str__(self) -> str:
    return self.name if self.name else self.id