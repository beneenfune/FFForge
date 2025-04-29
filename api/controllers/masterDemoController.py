from ..__init__ import db

"""
POST
GET
GET ALL
PATCH
DELETE
"""

class master_demo_inputs(db.Document):
    structure_name = db.StringField()
    temperature_range = db.StringField()

    def to_json(self):
        return {
            "structure_name": self.structure_name,
            "temperature_range": self.temperature_range
        }

print("\nCreate a Master Demo Input")
input = master_demo_inputs(
    structure_name = "pvdf",
    temperature_range = "0,1,2,3,4"
)
input.save()

print("\nFetch a Master Demo Input")
input = master_demo_inputs.objects(structure_name="pvdf").first()