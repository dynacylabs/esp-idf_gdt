#!/usr/bin/python3

import glob
import os
import subprocess

ghidra_project_basename = "gdt-"
gdt_library_prefix = "lib_"

# Get current dir
base_dir = os.getcwd()

# Paths
esp_idf_elfs_path = os.path.join(base_dir, "esp-idf_elfs")
ghidra_install_path = os.path.join(base_dir, "ghidra")
ghidra_gdt_path = os.path.join(base_dir, "ghidra-gdt")
ghidra_projects_path = os.path.join(base_dir, "ghidra_projects")
ghidra_headless_path = os.path.join(ghidra_install_path, "support", "analyzeHeadless")
gdt_libs_path = os.path.join(base_dir, "libraries")

if not os.path.exists(ghidra_projects_path):
    os.mkdir(ghidra_projects_path)
if not os.path.exists(gdt_libs_path):
    os.mkdir(gdt_libs_path)

release_list = ['release_v2.0',
                'release_v2.1',
                'release_v3.0',
                'release_v3.1',
                'release_v3.2',
                'release_v3.3',
                'release_v4.0',
                'release_v4.1',
                'release_v4.3',
                'release_v4.4',
                'release_v5.0',
                'release_v5.1']

os.chdir(esp_idf_elfs_path)

for release_dir in release_list:
    out_dir = os.path.join(base_dir, release_dir)
    if not os.path.exists(out_dir):
        os.mkdir(os.path.join(base_dir, release_dir))
    gdt_lib_file = os.path.join(gdt_libs_path, (gdt_library_prefix + release_dir + ".gdt"))

    os.chdir(os.path.join(esp_idf_elfs_path, release_dir))
    elf_glob = glob.glob('*.elf')
    for index, elf in enumerate(elf_glob):
        elf_path = os.path.normpath(os.path.join(esp_idf_elfs_path, release_dir, elf))
        ghidra_project_name = ghidra_project_basename + release_dir + "-" + elf
        # subprocess.run(["touch", os.p])  # Will always create

        if index == 0:
            # subprocess.run(["touch", gdt_lib_file])
            # First elf for library, must create lib first
            command = [ghidra_headless_path,
                       ghidra_projects_path,
                       ghidra_project_name,
                       "-import", elf_path,
                       "-scriptPath", ghidra_gdt_path,
                       "-postScript", "ExportGDT.py", out_dir, elf.replace('.elf', '.gdt'),
                       "-postScript", "ExportGDT.py", gdt_libs_path, gdt_lib_file]
        else:
            # Lib should exist
            command = [ghidra_headless_path,
                       ghidra_projects_path,
                       ghidra_project_name,
                       "-import", elf_path,
                       "-scriptPath", ghidra_gdt_path,
                       "-postScript", "ExportGDT.py", out_dir, elf.replace('.elf', '.gdt'),
                       "-postScript", "ExportGDTLibrary.py", gdt_libs_path, gdt_lib_file]

        subprocess.run(command)
