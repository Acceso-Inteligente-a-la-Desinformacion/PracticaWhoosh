# SEARCH ENGINE WHOOSH
import whoosh
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD
from whoosh.qparser import QueryParser
from whoosh.index import create_in,open_dir, exists_in
from whoosh import query

import os

class SEW:
    def __init__(self, indexDir: str, schema: type(Schema)):

        self.indexDir = indexDir

        if not os.path.exists(self.indexDir):
            os.mkdir(self.indexDir)

        self.schema = schema

    def createIndex(self, docsDir: str, addDoc: callable):
        def create():
            ix = create_in(self.indexDir, schema=self.schema)
            writer = ix.writer()

            i=0
            for doc in os.listdir(docsDir):
                docPath = os.path.join(docsDir, doc)

                if not os.path.isdir(docPath):
                    addDoc(writer, docsDir, doc)

                    i+=1
                    
            writer.commit()

            return i, ""
        
        if not os.path.exists(docsDir):
            return 0, "No existe el directorio de documentos " + docsDir
        else:
            return create()
        
    def query(self, parameter, value, callback: callable):
        ix=open_dir(self.indexDir)    
        with ix.searcher() as searcher:
            myquery = QueryParser(parameter, ix.schema).parse(str(value))
            results = searcher.search(myquery,limit=None)
            callback(results)
        
    def getAll(self, callback: callable):
        ix=open_dir(self.indexDir)
        with ix.searcher() as searcher:
            callback(searcher.search(query.Every()))

