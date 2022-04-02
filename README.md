# My little collection of SaltStack Config RPC scripts

## assign_rbac_role_env_folder
(I know name is horrible) this grants SaltStack's provided Role with RBAC permission access for files in Saltstack backend, either to all files in the specififed environment or to files in the optionally specified folder and its subfolders. By default assignes both Read and Discover grants.

Just run python3 assign_rbac_role_env_folder.py --help to have an understanding of required and optional arguments
