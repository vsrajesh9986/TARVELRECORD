import mysql.connector as mysql

db = mysql.connect(
    host='localhost',
    user='root',
    password='user',
    database='TravelRecord'
)

class TravelRecord:
    def __init__(self, history_id, individual_name, destination, travel_date=None, return_date=None):
        self.history_id = history_id
        self.individual_name = individual_name
        self.destination = destination
        self.travel_date = travel_date
        self.return_date = return_date

    def __repr__(self):
        return (f"TravelRecord(history_id={self.history_id}, "
                f"individual_name='{self.individual_name}', "
                f"destination='{self.destination}', "
                f"travel_date='{self.travel_date}', "
                f"return_date='{self.return_date}')")

class TravelHistoryTracker:
    def createdb():
        try:
            mycursor.execute("CREEATED DATABASE RECORD")
        except Exception:
            print('Already created db')
    def useDB():
        try:
            mycursor.execute("USE RECORD")
            print("using DB")
        except Exception:
            print('Already use DB')
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_record(self, history_id, individual_name, destination, travel_date=None, return_date=None):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO travel_records (history_id, individual_name, destination, travel_date, return_date)
                VALUES (%s, %s, %s, %s, %s)
            """, (history_id, individual_name, destination, travel_date, return_date))
            self.db_connection.commit()
        except mysql.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def read_record(self, history_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM travel_records WHERE history_id = %s", (history_id,))
        record = cursor.fetchone()
        cursor.close()
        if record:
            return TravelRecord(*record)
        return "Record not found."

    def update_record(self, history_id, individual_name=None, destination=None, travel_date=None, return_date=None):
        cursor = self.db_connection.cursor()
        try:
            updates = []
            params = []

            if individual_name:
                updates.append("individual_name = %s")
                params.append(individual_name)
            if destination:
                updates.append("destination = %s")
                params.append(destination)
            if travel_date:
                updates.append("travel_date = %s")
                params.append(travel_date)
            if return_date:
                updates.append("return_date = %s")
                params.append(return_date)

            if updates:
                sql = f"UPDATE travel_records SET {', '.join(updates)} WHERE history_id = %s"
                params.append(history_id)
                cursor.execute(sql, tuple(params))
                self.db_connection.commit()
            else:
                return "No updates provided."
        except mysql.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def delete_record(self, history_id):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("DELETE FROM travel_records WHERE history_id = %s", (history_id,))
            self.db_connection.commit()
            if cursor.rowcount == 0:
                return "Record not found."
        except mysql.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    def analyze_travel_behaviors(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT destination, COUNT(*) FROM travel_records GROUP BY destination")
        result = cursor.fetchall()
        cursor.close()

        destination_count = {destination: count for destination, count in result}
        return destination_count

# Create an instance of TravelHistoryTracker
tracker = TravelHistoryTracker(db)

# Create a record
#tracker.create_record(91, 'Rajesh', 'Japan', '2023-01-01', '2024-02-10')


# Read a record
#record = tracker.read_record(99)
#print(record)

# Update a record
#tracker.update_record(99, destination='Canada')

# Read the updated record
#updated_record = tracker.read_record(99)
#print(updated_record)

# Delete a record
tracker.delete_record(99)


# Analyze travel behaviors
pattern = tracker.analyze_travel_behaviors()
print(pattern)