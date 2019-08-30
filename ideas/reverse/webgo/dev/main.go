package main

import (
	"fmt"
	"html/template"
	"net/http"
	"hash"
	"sync"
	"io/ioutil"
)

const Size = 2

var (
	X25 = &Conf{
		Poly: 0x1021, BitRev: true,
		IniVal: 0xffff, FinVal: 0xffff,
		BigEnd: false,
	}
	PPP    = X25
	Modbus = &Conf{
		Poly: 0x8005, BitRev: true,
		IniVal: 0xffff, FinVal: 0x0,
		BigEnd: false,
	}
	XModem = &Conf{
		Poly: 0x1021, BitRev: false,
		IniVal: 0x0000, FinVal: 0x0,
		BigEnd: true,
	}
	Kermit = &Conf{
		Poly: 0x1021, BitRev: true,
		IniVal: 0x0, FinVal: 0x0,
		BigEnd: false,
	}
)

type Conf struct {
	Poly   uint16 // Polynomial to use.
	BitRev bool   // Bit reversed CRC (bit-15 is X^0)?
	IniVal uint16 // Initial value of CRC register.
	FinVal uint16 // XOR CRC with this at the end.
	BigEnd bool   // Emit *bytes* most significant first (see Hash.Sum)?
	once   sync.Once
	table  *Table
	update func(uint16, *Table, []byte) uint16
}

func reverse(v uint16) uint16 {
	r := v
	s := uint(16 - 1)

	for v >>= 1; v != 0; v >>= 1 {
		r <<= 1
		r |= v & 1
		s--
	}
	r <<= s
	return r
}

func (c *Conf) makeTable() {
	if c.BitRev {
		c.table = MakeTable(reverse(c.Poly))
		c.update = Update
	} else {
		c.table = MakeTableNBR(c.Poly)
		c.update = UpdateNBR
	}
}

type Table [256]uint16

func MakeTable(poly uint16) *Table {
	t := new(Table)
	for i := 0; i < 256; i++ {
		crc := uint16(i)
		for j := 0; j < 8; j++ {
			if crc&1 == 1 {
				crc = (crc >> 1) ^ poly
			} else {
				crc >>= 1
			}
		}
		t[i] = crc
	}
	return t
}

func MakeTableNBR(poly uint16) *Table {
	t := new(Table)
	for i := 0; i < 256; i++ {
		crc := uint16(i) << 8
		for j := 0; j < 8; j++ {
			if crc&0x8000 != 0 {
				crc = (crc << 1) ^ poly
			} else {
				crc <<= 1
			}
		}
		t[i] = crc
	}
	return t
}

func Update(crc uint16, tab *Table, p []byte) uint16 {
	for _, v := range p {
		crc = tab[byte(crc)^v] ^ (crc >> 8)
	}
	return crc
}

func UpdateNBR(crc uint16, tab *Table, p []byte) uint16 {
	for _, v := range p {
		crc = tab[byte(crc>>8)^v] ^ (crc << 8)
	}
	return crc
}

type digest struct {
	crc  uint16
	conf *Conf
}

type Hash16 interface {
	hash.Hash
	Sum16() uint16
}

func New(c *Conf) Hash16 {
	c.once.Do(c.makeTable)
	return &digest{crc: c.IniVal, conf: c}
}

func (d *digest) Size() int { return Size }

func (d *digest) BlockSize() int { return 1 }

func (d *digest) Reset() { d.crc = d.conf.IniVal }

func (d *digest) Write(p []byte) (n int, err error) {
	d.crc = d.conf.update(d.crc, d.conf.table, p)
	return len(p), nil
}

func (d *digest) Sum16() uint16 { return d.crc ^ d.conf.FinVal }

func (d *digest) Sum(in []byte) []byte {
	s := d.Sum16()
	if d.conf.BigEnd {
		return append(in, byte(s>>8), byte(s))
	} else {
		return append(in, byte(s), byte(s>>8))
	}
}

func Checksum(c *Conf, data []byte) uint16 {
	c.once.Do(c.makeTable)
	return c.update(c.IniVal, c.table, data) ^ c.FinVal
}


// =========================================================
// ------------------------ MY CODE ------------------------
// =========================================================

func check_cookie( cookie string ) bool {
	//fmt.Println( "cookie: " + cookie )

	if len( cookie ) != 20 {
		return false
	}

	var parts [][] byte
	var elem [] byte
	var crcs [] uint16

	// split cookie to 2-byte parts
	for i := 0; i < len( cookie ); i += 2 {
		
		elem = append( elem, cookie[ i ] )
		elem = append( elem, cookie[ i + 1 ] )

		parts = append( parts, elem )
	}

	/* calc crc16 as:
		crcs[ i ] = cookie[:i*2 + 2 ]
	*/
	for i := 0; i < len( parts ); i++ {
		crc16sum := Checksum( X25, parts[ i ] )
		crcs = append( crcs, crc16sum )
	}
	// res = [61095 8049 42260 58053 36709 57072 6606 37799 4652 31540]
	
	// gen xor_keys
	var xor_keys [] uint16 

	for i := 0; i < len( crcs ); i++ {
		var tmp []byte
		tmp = append( tmp, cookie[ i ] )

		xor_keys = append( xor_keys, Checksum( X25, tmp ) )
	}

	valids := [10] uint16 { 49170, 5086, 13122, 9750, 15377, 20382, 25550, 29006, 31141, 40445 }

	for i := 0; i < len( valids ); i++ {
		if ( crcs[ i ] ^ xor_keys[ i ] ) != valids[ i ] {
			return false
		} 
	}

	return true
}

func index_handler( w http.ResponseWriter, r *http.Request ) {
	t, _ := template.ParseFiles( "templates/index.html" )
	c, err := r.Cookie( "asm_dev_test" )

	if err == nil {
		val := c.Value
		
		if check_cookie( val ) {
			//fmt.Println( "valid cookie!" )
			data, err := ioutil.ReadFile( "dev_journal.txt" )

			if err != nil {
				fmt.Println( "[-] Error in dev_journal.txt file open!" )
			} else {
				fmt.Fprintf( w, "dev_journal: %s", data )
				return
			}
		}
	}

	t.Execute( w, nil )
}

func login_handler( w http.ResponseWriter, r *http.Request ) {
	t, _ := template.ParseFiles( "templates/index.html" )
	t.Execute( w, nil )
}

func main() {
	// valid cookie - XK5eQBn2ovG8YcfCAfFI
	//check_cookie( "XK5eQBn2ovG8YcfCAfFI" )

	http.HandleFunc( "/", index_handler )
	http.HandleFunc( "/login", login_handler )
	http.ListenAndServe( ":7777", nil )
}