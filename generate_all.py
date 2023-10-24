#!/usr/bin/python3

import glob
import os
import subprocess

ghidra_project_basename = "rizzo-"
rizzo_out_child_base_dirname = "esp-idf-"

# Get current dir
base_dir = os.getcwd()

# Paths
esp_idf_elfs_path = os.path.join(base_dir, "esp-idf_elfs")
ghidra_install_path = os.path.join(base_dir, "ghidra")
ghidra_rizzo_path = os.path.join(base_dir, "ghidra-gdt")
ghidra_projects_path = os.path.join(base_dir, "ghidra_projects")
ghidra_headless_path = os.path.join(ghidra_install_path, "support", "analyzeHeadless")

ghidra_project_basename = "rizzo-"
if not os.path.exists(ghidra_projects_path):
    os.mkdir(ghidra_projects_path)
done_glob = glob.glob('release_v*')

os.chdir(esp_idf_elfs_path)
release_glob = glob.glob('release_v*')
for release_dir in release_glob:
    if release_dir not in done_glob:
        out_dir = os.path.join(base_dir, release_dir)
        if not os.path.exists(out_dir):
            os.mkdir(os.path.join(base_dir, release_dir))
     
        os.chdir(os.path.join(esp_idf_elfs_path, release_dir))
        elf_glob = glob.glob('*.elf')
        for elf in elf_glob:
            elf_path = os.path.normpath(os.path.join(esp_idf_elfs_path, release_dir, elf))
            out_file = os.path.join(out_dir, elf.replace('.elf', '.gdt'))
            ghidra_project_name = ghidra_project_basename + release_dir + "-" + elf
            subprocess.run(['touch', out_file])
            command = [ghidra_headless_path,
                       ghidra_projects_path,
                       ghidra_project_name,
                       "-import", elf_path,
                       "-scriptPath", ghidra_rizzo_path,
                       "-postScript", "ExportGDT.py", out_file] 

            subprocess.run(command)
