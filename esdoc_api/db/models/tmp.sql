CREATE SEQUENCE docs."tbl_document_sub_project_id_seq"
  INCREMENT 1
  MINVALUE 1
  MAXVALUE 9223372036854775807
  START 36705
  CACHE 1;
ALTER TABLE docs."tbl_document_sub_project_id_seq"
  OWNER TO postgres;
GRANT ALL ON TABLE docs."tbl_document_sub_project_id_seq" TO postgres;
GRANT SELECT, USAGE ON TABLE docs."tbl_document_sub_project_id_seq" TO esdoc_db_user;



CREATE TABLE docs.tbl_document_sub_project
(
  id integer NOT NULL DEFAULT nextval('docs."tbl_document_sub_project_id_seq"'::regclass),
  project_id integer NOT NULL,
  sub_project_id integer NOT NULL,
  document_id integer NOT NULL,
  CONSTRAINT tbl_document_sub_project_pkey PRIMARY KEY (id),
  CONSTRAINT "tbl_document_sub_project_document_id_fkey" FOREIGN KEY (document_id)
      REFERENCES docs.tbl_document (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "tbl_document_sub_project_project_id_fkey" FOREIGN KEY (project_id)
      REFERENCES vocab.tbl_project (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "tbl_document_sub_project_sub_project_id_fkey" FOREIGN KEY (sub_project_id)
      REFERENCES vocab.tbl_project (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT "tbl_document_sub_project_project_id_document_id_sub_project_id_key" UNIQUE (project_id, document_id, sub_project_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE docs.tbl_document_sub_project
  OWNER TO postgres;
GRANT ALL ON TABLE docs.tbl_document_sub_project TO postgres;
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLE docs.tbl_document_sub_project TO esdoc_db_user;