import subprocess 
import sys 
import glob 
import os 
     
class magpie_workflow:
    def __init__(self):
        self.poscars_dir = './input_poscars/'
        self.poscars_ext = '*'
        self.prop_dir    = './software/Magpie/lookup-data/' 
        self.magpie_exec = ['java', '-jar', './software/Magpie/dist/Magpie.jar']
        self.poscars_dir = './input_poscars/'
        self.GEN_TAG     = ''
    def OWrite(self,s): 
        with open('./out.workflow.txt','a') as fout: 
            fout.write(s) 
        print(s) 
        sys.stdout.flush()     
     
    def run_magpie(self): 
        self.runfile_ext = [self.mag_ip_file+'.in','|', 'tee', self.mag_ip_file+'.out'] 
     
        with open('./out.workflow.txt','a') as fout: 
            with open('./err.worksflow.txt','a') as ferr: 
                out=subprocess.call(self.magpie_exec+runfile_ext, stdout=fout, stderr=ferr) 
        sys.stdout.flush() 
     
     
    def input_gen(self): 
        self.mag_feats_file  = './'+self.GEN_TAG+'features_generated_magpie.csv' 
        magpie_comms = ['data = new data.materials.CrystalStructureDataset', \ 
                        'timer start', 'data import '+self.poscars_dir, 'timer elapsed', \ 
                        'data attributes properties directory '+self.prop_dir, \ 
                        'data attributes properties add set general', \ 
                        'data target local_reference', \ 
                        'attr = new utility.tools.BatchAttributeGenerator 1000 DelimitedOutput ,', \ 
                        'timer start', 'attr write '+self.mag_feats_file+' $data', \ 
                        'timer elapsed', 'exit'] 
     
        self.mag_ip_file = './'+self.GEN_TAG+'generate-attributes' 
        with open(self.mag_ip_file+'.in','w') as fout: 
            fout.write('\n'.join(magpie_comms)) 
     
    def reference_gen(self): 
        if not self.poscars_ext.startswith('*'): 
            self.poscars_ext = '*'+self.poscars_ext 
     
        files_list = glob.glob(os.path.join(self.poscars_dir,self.poscars_ext)) 
        files_list = [' '.join([item.split('/')[-1],str(i)]) for i,item in enumerate(files_list)]
        title      = ' '.join(['filename','local_reference'])
        with open(os.path.join(self.poscars_dir+'properties.txt'),'w') as fout:
            fout.write('\n'.join(title+files_list))

    def post_process(self):
        if not os.path.isfile(self.feats_file+'.out'):
            print('magpie output file not found. Run Magpie first')
            return
        data = open(self.mag_feats_file,'r').read().strip().split('\n')
        data = [item.strip().split(',') for item in data]
        title = ','.join(['filename']+data[0][:-1])
        self.processed_feats_file = './'+self.GEN_TAG+'features_processed_final.csv'

        ref_data = open(os.path.join(self.poscars_dir+'properties.txt'),'r').read().strip().split('\n')[1:]
        for i,item in enumerate(data):
            out_index = int(round(float(item[-1])))
            data[i]   = ','.join([ref_data[out_index].strip().split(' ')[0]] + item[:-1])

        with open(self.processed_feats_file,'w') as fout:
            data = '\n'.join([title]+data)
            fout.write(data)
         
     
     
def main(): 
    print('Beginning the workflow')
    workflow = magpie_workflow()
    workflow.reference_gen()
    workflow.input_gen()
    workflow.run_magpie()
    workflow.post_process()
    print('Done')

     
