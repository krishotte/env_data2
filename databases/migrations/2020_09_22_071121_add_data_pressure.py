from orator.migrations import Migration


class AddDataPressure(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('data') as table:
            table.float('pressure')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('data') as table:
            table.drop_column('pressure')
