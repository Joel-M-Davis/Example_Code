
# coding: utf-8

# In[1]:


"""
Vinyl Records Database

Interactive program allows users to look up records in collection by Artist Name, Album Name, etc.
Add new records, delete records, etc...
"""

import sqlite3

db_file = "vinylrecords.sqlite"

#main table for albums
albums_table = "albums"
id_col = "id"
cat_num_col = "cat_num"
name_col = "name"
artist_id_col = "artist_id"
release_year_col = "release_year"
print_year_col = "print_year"
genre_id_col = "genre1_id"
label_id_col = "label_id"

#other tables and columns
artists_table = "artists"
songs_table = "songs"
labels_table = "labels"
genres_table = "genres"
album_id_col = "album_id"


#Get the next ID in a table if an insert statement is needed
def get_next_id(c, table):
    c.execute("SELECT * FROM {}".format(table))
    maximum = 0
    for row in c:
        if row[0] > maximum:
            maximum = row[0]
    return maximum + 1

#Ask a user a question that requres input. condition_string establishes valid inputs. Returns user's input
def ask_user(question, condition_string):
    while True:
        try:
            choice = input(question)
            if eval(condition_string):
                print("Invalid choice! \n")
                continue
        except:
            print("Invalid choice! \n")
            continue
        else:
            return choice
        
#ask user if they would like to return to main menu or quit
def return_or_quit():
    print("1. Return to Main Menu")
    print("2. Quit")
    choice = int(ask_user("What would you like to do? ", "int(choice) not in [1,2]"))

    if choice == 2:
        return False
    else: 
        return True
        
def add_record(cursor, connection):
    print("Enter 'Q' or 'Quit' in any field to cancel adding record.")

    while True:
        #list of attributes to enter into database
        stats = []
        
        #determine album id #
        cursor.execute("SELECT * FROM albums ORDER BY id")
        stats.append(get_next_id(cursor, albums_table))
        
        #determine catalog number
        stats.append(ask_user("What is the album catalog number? ", "False"))
        if stats[1] in ["q", "Q", "Quit", "quit"]:
            print("Cancelling adding record")
            break
 
        #determine album name
        stats.append(ask_user("What is the album name? ", "False"))
        if stats[2] in ["q", "Q", "Quit", "quit"]:
            print("Cancelling adding record")
            break
        
        #determine artist id
        artist = ask_user("What is the artist name? ", "False")
        if artist in ["q", "Q", "Quit", "quit"]:
            print("Cancelling adding record")
            break
        cursor.execute("SELECT * FROM artists WHERE name LIKE '{}'".format(artist))
        artists = cursor.fetchall()
        if artists != []:
            for row in artists:
                stats.append(row[0])
        else:
            stats.append(get_next_id(cursor, artists_table))
            #create new artist in artists table if artist not seen before
            cursor.execute("INSERT INTO artists VALUES({}, '{}')".format(stats[3], artist))  
            
            
        #determine release year
        stats.append(ask_user("What is the album release year? ", "float(choice) < 1900"))
        if stats[4] in ["q", "Q", "Quit", "quit"]:
            print("Cancelling adding record")
            break
        
        #determine print year
        stats.append(ask_user("What year was the album printed? ", "float(choice) < 1900"))
        if stats[5] in ["q", "Q", "Quit", "quit"]:
            print("Cancelling adding record")
            break
        
        #determine genre id
        genre = ask_user("What is the genre of the album? ", "False")
        if genre in ["q", "Q", "Quit", "quit"]:
            print("Cancelling adding record")
            break
        cursor.execute("SELECT * FROM genres WHERE name LIKE '{}'".format(genre))
        genres = cursor.fetchall()
        if genres != []:
            for row in genres:
                stats.append(row[0])
        else:
            stats.append(get_next_id(cursor, genres_table))
            #create new genre in genres table if genre not seen before
            cursor.execute("INSERT INTO genres VALUES({}, '{}')".format(stats[6], genre)) 
            
        #determine label id
        label = ask_user("What is the album label? ", "False")
        if label in ["q", "Q", "Quit", "quit"]:
            print("Cancelling adding record")
            break
        cursor.execute("SELECT * FROM labels WHERE name LIKE '{}'".format(label))
        labels = cursor.fetchall()
        if labels != []:
            for row in labels:
                stats.append(row[0])
        else:
            stats.append(get_next_id(cursor, labels_table))
            #create new label in labels table if label not seen before
            cursor.execute("INSERT INTO labels VALUES({}, '{}')".format(stats[7], label))  
            
        #determine songs on album
        song_count = int(ask_user("How many songs are on the album? ", "float(choice) < 0"))
        songs = []
        print("Please enter the names of the songs:")
        for song in range(song_count):
            songs.append(ask_user("Song {}: ".format(song + 1), "False"))
            if songs[song] in ["q", "Q", "Quit", "quit"]:
                print("Cancelling adding record")
                break
                
        #check if album already in database
        cursor.execute("SELECT * FROM {}".format(albums_table))
        match_list = stats
        match_list[-3], match_list[-4] = int(match_list[-3]), int(match_list[-4])
        match = False
        for x in cursor:
            if tuple(match_list)[1:] == x[1:]:
                match = True
        if match == True:
            print("Album Already in Database.")
            if ask_user("Search again? ", "choice not in ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'N', 'n']") not in ['Yes', 'yes', 'y', 'Y']:
                break
        else:
            #add new info to database
            cursor.execute("INSERT INTO albums VALUES({}, '{}', '{}', {}, {}, {}, {}, {})".format(stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], stats[6], stats[7]))
            cursor.execute("SELECT * FROM songs ORDER BY id")
            new_id = get_next_id(cursor, songs_table)
            for song in songs:
                cursor.execute("INSERT INTO songs VALUES({}, '{}', {}, {})".format(new_id, song, stats[0], stats[3]))
                new_id += 1
            connection.commit()

            if ask_user("Album successfully added to database. Add another? ", "choice not in ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'N', 'n']") not in ['Yes', 'yes', 'y', 'Y']:
                break
            
    return return_or_quit()

def connect_to_db():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    print("Connected to Database")
    try:
        #create albums table
        c.execute("CREATE TABLE {} ({} INTEGER PRIMARY KEY, {} TEXT,{} TEXT, {} INTEGER, {} INTEGER, {} INTEGER, {} INTEGER, {} INTEGER)".format(albums_table, id_col, cat_num_col, name_col, artist_id_col, release_year_col, print_year_col, genre_id_col, label_id_col))
    except:
        pass

    try:
        #create artists table 
        c.execute("CREATE TABLE {} ({} INTEGER PRIMARY KEY, {} TEXT)".format(artists_table, id_col, name_col))
    except:
        pass

    try:
        #create genres table 
        c.execute("CREATE TABLE {} ({} INTEGER PRIMARY KEY, {} TEXT)".format(genres_table, id_col, name_col))
    except:
        pass

    try:
        #create labels table
        c.execute("CREATE TABLE {} ({} INTEGER PRIMARY KEY, {} TEXT)".format(labels_table, id_col, name_col))
    except:
        pass
    
    try:
        #create songs table
        c.execute("CREATE TABLE {} ({} INTEGER PRIMARY KEY, {} TEXT, {} INTEGER, {} INTEGER)".format(songs_table, id_col, name_col, album_id_col, artist_id_col))
        print("Tables created!")
    except:
        pass
    
    return c, conn    

    
def search_records(cursor):
    while True:
        print("You can search by album name, artist, catalog number, genre, label, song title, release year or print year.")
        print("Enter 'Q' or 'Quit' to cancel searching.")
        keyword = ask_user("Search Term: ", "False")
        if keyword in ["q", "Q", "Quit", "quit"]:
            break
        album_ids = []
        
        #checck album names, catalog numbers, release years and print years
        cursor.execute("SELECT id, name, cat_num, release_year, print_year FROM albums")
        for row in cursor:
            if keyword.lower() in row[1].lower() or keyword.lower() in row[2].lower() or keyword.lower() in str(row[3]) or keyword.lower() in str(row[4]):
                album_ids.append(row[0])      

        #checck artist names
        cursor.execute("SELECT id, name FROM artists")
        artists = []
        for row in cursor:
            if keyword.lower() in row[1].lower():
                artists.append(row[0])
        cursor.execute("SELECT id, artist_id FROM albums")
        for row in cursor:
            if row[1] in artists:
                album_ids.append(row[0])
     
        #check genres
        cursor.execute("SELECT id, name FROM genres")
        genres = []
        for row in cursor:
            if keyword.lower() in row[1].lower():
                genres.append(row[0])
        cursor.execute("SELECT id, {} FROM albums".format(genre_id_col))
        for row in cursor:
            if row[1] in genres:
                album_ids.append(row[0])
                
        #check labels
        cursor.execute("SELECT id, name FROM labels")
        labels = []
        for row in cursor:
            if keyword.lower() in row[1].lower():
                labels.append(row[0])
        cursor.execute("SELECT id, label_id FROM albums")
        for row in cursor:
            if row[1] in labels:
                album_ids.append(row[0])

        #check song titles
        cursor.execute("SELECT name, album_id FROM songs")
        for row in cursor:
            if keyword.lower() in row[0].lower():
                album_ids.append(row[1])
                
        if album_ids == []:
            print("No Matching Albums.")
            if ask_user("Search again? ", "choice not in ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'N', 'n']") not in ['Yes', 'yes', 'y', 'Y']:
                break
        else:
            ids_set = set(album_ids)
            ids = "("
            for x in ids_set:
                ids += str(x)
                ids += ", "
            ids = ids[0:-2]
            ids += ")"


            #query database for those albums
            cursor.execute("SELECT albums.name, artists.name, cat_num, labels.name, genres.name, release_year, print_year FROM albums, artists, labels, genres WHERE albums.artist_id = artists.id AND albums.genre1_id = genres.id AND albums.label_id = labels.id AND albums.id IN {}".format(ids))
            for x in cursor:
                print(x)

            if ask_user("Search again? ", "choice not in ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'N', 'n']") not in ['Yes', 'yes', 'y', 'Y']:
                break    

    return return_or_quit()


def search_other(cursor, table):
    while True:
        print("Enter the name of the {}, or just hit enter to see all {}s.".format(table, table))
        print("Enter 'Q' or 'Quit' to cancel searching.")
        keyword = ask_user("Search Term: ", "False")
        if keyword in ["q", "Q", "Quit", "quit"]:
            break  

        #display genre names
        print("Matching {}s:".format(table))
        cursor.execute("SELECT name FROM {}s".format(table))
        for row in cursor:
            if keyword.lower() in row[0].lower():
                print(row[0])
                
        if ask_user("Search again? ", "choice not in ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'N', 'n']") not in ['Yes', 'yes', 'y', 'Y']:
                break
    
    return return_or_quit()
    
def delete_record(cursor, connection):
    while True:
        cat_num = ask_user("What is the catalog number of the album?", "False")
        cursor.execute("SELECT albums.name, artists.name, cat_num, labels.name, genres.name, release_year, print_year FROM albums, artists, labels, genres WHERE albums.artist_id = artists.id AND albums.genre1_id = genres.id AND albums.label_id = labels.id AND cat_num LIKE {}".format(cat_num))
        results = cursor.fetchall()
        count = len(results)
        if count == 0:
            print("No records found.")
            if ask_user("Search again? ", "choice not in ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'N', 'n']") not in ['Yes', 'yes', 'y', 'Y']:
                break  
        else:
            if ask_user("Are you sure you want to delete this record? \n{}\n".format(results[0]), "choice not in ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'N', 'n']") not in ['Yes', 'yes', 'y', 'Y']:
                if ask_user("Would you like to delete another record? ", "choice not in ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'N', 'n']") not in ['Yes', 'yes', 'y', 'Y']:
                    break
            else:
                cursor.execute("SELECT id FROM albums WHERE cat_num LIKE {}".format(cat_num))
                delete_id = cursor.fetchone()[0]
                cursor.execute("DELETE FROM albums WHERE id = {}".format(delete_id))
                connection.commit()
                
                if ask_user("Delete another record? ", "choice not in ['Yes', 'yes', 'y', 'Y', 'No', 'no', 'N', 'n']") not in ['Yes', 'yes', 'y', 'Y']:
                    break 
    
    return return_or_quit()
        

def main():
    #open the database
    cursor, connection = connect_to_db()
    print("Welcome to Joel's Vinly Record Database")
    active = True
    
    while active:
        print("1. Add Record")
        print("2. Search for Records")
        print("3. Search for Artists")
        print("4. Search for Songs")
        print("5. Search for Genres")
        print("6. Search for Labels")
        print("7. Delete Record")
        print("8. Quit")
        choice = ask_user("What would you like to do? ", "int(choice) not in [1,2,3,4,5,6,7,8]")
        
        if int(choice) == 8:
            active == False
            break
        elif int(choice) == 7:
            active = delete_record(cursor,connection)
        elif int(choice) == 6:
            active = search_other(cursor, "label")
        elif int(choice) == 5:
            active = search_other(cursor, "genre")
        elif int(choice) == 4:
            active = search_other(cursor, "song")
        elif int(choice) == 3:
            active = search_other(cursor, "artist")
        elif int(choice) == 2:
            active = search_records(cursor)
        else:
            active = add_record(cursor, connection)
        
    print("See you later!")
    connection.close()
    
    


# In[2]:


main()

