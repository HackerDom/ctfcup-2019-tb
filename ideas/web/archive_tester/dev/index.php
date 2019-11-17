<?php

#include( ".secret_flag_file_05f85a4b8c8927fbbfd3f664a3204ecd081cc307e52c8822775d7e5b42056110.php" );

function gen_name() 
{
    $alph = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'; 
    $str = ''; 
  
    for ( $i = 0; $i < 10; $i++ ) 
    { 
        $index = rand( 0, strlen( $alph ) - 1 ); 
        $str .= $alph[ $index ]; 
    }
  
    return $str; 
} 

echo "Free archive tester
<form method='post' enctype='multipart/form-data'><input type='file' name='zipfile'/>
 
<input type='submit' name='submit' value='Upload'/></form>
 
";

if ( $_FILES[ 'zipfile' ][ 'name' ] ) 
{
  
	if ( $_FILES['zipfile']['size'] > 10240 ) 
 	{
 		echo "File above max size of 10kb";
		die();
 	}

 	$tmp_file = '/var/www/html/tmp/upload_' . gen_name();

 	exec( 'unzip -o ' . $_FILES[ 'zipfile' ][ 'tmp_name' ] . ' -d ' . $tmp_file );
 	echo "Zip contents: <br>";

 	passthru( "cat $tmp_file/* 2>&1" );
 	exec( "rm -rf $tmp_file" );
}

?>