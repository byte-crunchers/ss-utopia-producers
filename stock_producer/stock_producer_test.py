from stock_producer import *
import glob #used for its file searching wildcard support

def test_clean(): #tests the clean function by adding a test file to stock_dump, 
                    #calling clean, and making sure said file is deleted
    #lets first verify that stock_dump exists
    if(not os.path.isdir("stock_dump")):
        os.mkdir("stock_dump")
    
    open('stock_dump/clean_test', 'w') #creates test file if none exist
    assert os.path.isfile('stock_dump/clean_test') #make sure the file really is there
    clean()
    assert not os.path.isfile('stock_dump/clean_test') #assert file has been deleted


def test_produce(): #this test only makes sure that produce() at least generates files
    clean() #blank slate
    produce(100, 0)
    assert glob.glob("stock_dump/*100.json")
    assert not glob.glob("stock_dump/*101.json")
    clean() #leave it blank again


    

    