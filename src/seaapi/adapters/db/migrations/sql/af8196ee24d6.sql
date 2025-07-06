DELETE FROM groups;
DELETE FROM user_groups;
INSERT INTO groups (id, name, "default") VALUES (1, 'Administrador', false);
INSERT INTO groups (id, name, "default") VALUES (2, 'Usuário', true);