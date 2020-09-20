from orator.migrations import Migration


class CreateDataTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('data') as table:
            table.increments('id')
            table.datetime('timestamp')
            table.float('battery')
            table.float('temperature')
            table.float('humidity')

            table.integer('device_id').unsigned()
            table.foreign('device_id').references('id').on('devices')

            # table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('data')
