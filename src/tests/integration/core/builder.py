import os
import shutil
from subprocess import check_output
from jinja2 import Template


class Builder:
    def __init__(self, 
                 fift_path,
                 fift_executer_path,
                 func_compiler_path, 
                 out_path, 
                 secret_path, 
                 logger=None,
                 log_path='../../logs',
                 **kwargs):
        self.logger = logger  # TODO
        self.fift_path = fift_path
        self.fift_executer_path = fift_executer_path
        self.func_compiler_path = func_compiler_path
        self.out_path = out_path
        self.secret_path = secret_path

        os.environ['FIFTPATH'] = os.path.join(self.fift_path, 'lib')


    def clear_out(self):
        print(f'Clear output dir {self.out_path}...')
        if os.path.exists(self.out_path):
            shutil.rmtree(self.out_path)
        os.mkdir(self.out_path)


    def compile_sources(self, src_path, src_files, **kwargs):
        print(f'Compile *.fc sources from {src_path} ...')

        if not os.path.exists(self.out_path):
            os.mkdir(self.out_path)

        for code_file in src_files:
            file_group = src_files[code_file]
            in_files = [os.path.join(src_path, file) for file in file_group]
            out_file = os.path.join(self.out_path, f'{code_file}-code.fif')

            print(f'  > compile {out_file}')
            check_output([self.func_compiler_path, '-o', out_file, '-SPA', *in_files])

        print('Compile sources: DONE')


    def build_templates(self, tif_path, tif_files, **kwargs):
        print(f'Build *.tif templates from {tif_path} ...')

        for tif_target in tif_files:
            if len(tif_target) == 1:
                tpl_file = os.path.join(tif_path, tif_target[0])
                out_file = os.path.join(self.out_path, tif_target[0])
                shutil.copyfile(tpl_file, out_file)
                continue

            target_file, base_file = tif_target
            tpl_file = os.path.join(tif_path, target_file)
            out_file = os.path.join(self.out_path, target_file.split('.')[0] + '.tif')

            with open(tpl_file, 'r') as f:
                target_template = f.read()
                self.render_template(os.path.join(tif_path, base_file),
                                     params={'request_body': target_template},
                                     out_file=out_file)

        print('Build templates: DONE')


    def render_template(self, tpl_file, params, out_file, decorate_str=False):
        print(f'  > building {out_file} template...')

        if decorate_str:
            for p in params:
                param = params[p]
                if isinstance(param, str):
                    params[p] = f'"{param}"'

        with open(tpl_file, 'r') as f:
            template = f.read()
            result = Template(template).render(**params)

        with open(out_file, 'w') as f:
            f.writelines(result)

        print(f'  > building {out_file} template: DONE')


    def execute_fif(self, fif_file, verbose=False):
        print(f'  > execute fift script {fif_file}...')

        result = check_output([self.fift_executer_path, '-s', fif_file])
        if verbose:
            print(result)

        print(f'  > execute fift script {fif_file}: DONE')
