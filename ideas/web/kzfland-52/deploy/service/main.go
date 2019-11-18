package main

import (
	"html/template"
	"net/http"
	"os"
	"strconv"
	"io"

	"strings"

	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"github.com/jmoiron/sqlx"

)

func download_handler( w http.ResponseWriter, r *http.Request ) {
	Openfile, err := os.Open( "templates/d4d02ab944e79608ee06b09d00eb1132" )
	defer Openfile.Close()

	if err != nil {
		http.Error( w, "File not found.", 404 )
		return
	}

	FileHeader := make( []byte, 512 )
	
	Openfile.Read( FileHeader )
	FileContentType := http.DetectContentType( FileHeader )

	FileStat, _ := Openfile.Stat()
	FileSize := strconv.FormatInt( FileStat.Size(), 10 )

	w.Header().Set( "Content-Disposition", "attachment; filename=binary" )
	w.Header().Set( "Content-Type", FileContentType )
	w.Header().Set( "Content-Length", FileSize )

	Openfile.Seek( 0, 0 )
	io.Copy( w, Openfile )
}

func robots_hanlder( w http.ResponseWriter, r *http.Request ) {
	t, _ := template.ParseFiles( "templates/robots.txt" )
	t.Execute( w, nil )
}

func dev_handler( w http.ResponseWriter, r *http.Request ) {
	t, _ := template.ParseFiles( "templates/index.html" )
	w.Header().Set( "Files", "robots.txt, index.html, d4d02ab944e79608ee06b09d00eb1132" )
	t.Execute( w, nil )
}

func index_handler( w http.ResponseWriter, r *http.Request ) {
	t, _ := template.ParseFiles( "templates/index.html" )
	t.Execute( w, nil )
}

func isvalid( buf string ) bool {

	buf = strings.ToLower( buf )

	black_list := []string{ "and", "select", "drop", "time", 
		"from", "where", "union", 
		")", "(", "func", "sqlite", 
		"schema", ";", "`", "hex", 
		"sleep", "||", "substr", "length", "cast",
		"attach", "database", "as", "create", "table",
		"insert", "into", "values", "load_extension", 
		"not" }

	for _, elem := range black_list {
		if strings.Contains( buf, elem ) {
			return false
		}
	}

	return true
}

func login_handler( w http.ResponseWriter, r *http.Request ) {
	
	if r.Method == "POST" {

		if err := r.ParseForm(); err != nil {
			return
		}
		
		name := r.FormValue( "username" )
		pass := r.FormValue( "password" )
 
		if !( isvalid( name ) ) {
			fmt.Fprintf( w, "[-] Invalid username!" )
			return
		}
	
		// database, _ := sql.Open( "mysql", "root:toor@/go_users" ) 
		query := "SELECT password FROM users WHERE username ='" + name + "'" 

		conn, err := sqlx.Connect( "mysql", "root:toor@tcp(localhost:3306)/go_users" )
	
		if err != nil {
			panic(err)
		}

		var password string
		conn.Get( &password, query )

		conn.Close()

		if pass == password {
			fmt.Fprintf( w, "{+} Correct pass!" )
			return
		}

		fmt.Fprintf( w, "{-} Incorrect pass!" )

	} else {
		t, _ := template.ParseFiles( "templates/index.html" )
		t.Execute( w, nil )
	}
}

func main() {

	// DATABASE INIT
	//database, _ := sql.Open( "mysql", "root:toor@/go_users" )

	conn, err := sqlx.Connect( "mysql", "root:toor@tcp(localhost:3306)/go_users" )
	
	if err != nil {
		panic(err)
	}
	
	conn.MustExec( "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, secret TEXT)")

	_, err = conn.Exec( "INSERT INTO users VALUES ('revker', 'kerrev', 'Cup{23546ca577fb70941f62da30bb93605fdd22f9d4d072b1674372b0be2cff7231}')" )

	if err != nil {
		panic(err)
	}

	conn.Close()

	http.HandleFunc( "/", index_handler )
	http.HandleFunc( "/login", login_handler )
	http.HandleFunc( "/robots.txt", robots_hanlder )
	http.HandleFunc( "/dev", dev_handler ) 
	http.HandleFunc( "/d4d02ab944e79608ee06b09d00eb1132", download_handler )

	http.ListenAndServe( ":7777", nil )
}