from data import alchemy
from . import episode


class ShowModel(alchemy.Model):
    __tablename__ = "shows"  # o modelo irá referenciar esta tabela

    # criada coluna id do tipo int e que é primary key
    id = alchemy.Column(alchemy.Integer, primary_key=True)

    # criada coluna name do tipo string de no máximo 80 caracteres
    name = alchemy.Column(alchemy.String(80))

    # carregar automaticamente os episodios
    episodes = alchemy.relationship(episode.EpisodeModel, lazy='dynamic')

    # lazy irá carregar os episodios somente conforme for utiliza-los

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name, 'episodes': [episode.json() for episode in self.episodes.all()]}

    def save_to_db(self):
        alchemy.session.add(self)  # adicionando a sessão a memoria
        alchemy.session.commit()  # inserindo os dados no db

    def delete_from_db(self):
        alchemy.session.delete(self)
        alchemy.session.commit()

    def update(self):
        alchemy.session.update(self)
        alchemy.session.commit()

    @classmethod
    # não irá referenciar apenas uma linha mas sim o modelo como um todo
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
