from orator.migrations import Migration


class CreateDevicesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('devices') as table:
            table.increments('id')
            table.string('name').unique()
            table.string('description').nullable()

            # table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('devices')
