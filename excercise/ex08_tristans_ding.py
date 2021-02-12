import pandas as pd
import timeit


def msp_to_df(
        input_file,
        max_seq_len=30,
        min_ce=36,  # todo: set back to 36
        max_ce=40,
        mz_min=135,
        mz_max=1400,
):
    """
    Function to read spectrum data from .msp file and convert to dataframe.
    Args:
        input_file (str): path to .msp file
        max_seq_len (int): maximum acceptable sequence length
        min_ce (int): minimum collision energy of spectra to be included in df
        max_ce (int): maximum collision energy of spectra to be included in df
        mz_min (int): lower boundary for m/z to be included in df
        mz_max (int): lower boundary for m/z to be included in df

    Returns:
        df (pd.DataFrame or np.array): spectrum information within defined parameters [n_spectra, n_features]
        seqs (pd.DataFrame or np.array): sequences
    """

    with open(input_file) as file:
        msp_data = file.read()  # --> str

    # split spectra from one another
    spectra = msp_data.split('\n\n')  # split @ empty lines --> list:17852
    spectra = spectra[:-1]  # get rid of empty spectrum

    sq_lst = []
    data = []
    # mz_lst = []
    # it_lst = []
    cols = []
    # big_df = pd.DataFrame()+
    frame = pd.DataFrame()

    for i, spectrum in enumerate(spectra):
        # find collision energy
        line = spectrum.split('\n')[0]  # slice in lines and choose the first one
        ce = float(line.split('_')[-1][:-2])  # take the last _ separated piece but leave the unit (eV)

        # select collision energies based on provided thresholds
        if min_ce <= ce <= max_ce:
            # find sequence length before the first /
            sq = spectrum.split('/')[0][6:]  # cut the first 3 characters (Name:)
            # print(sq)

            # select sequences short enough to fit the requirements
            if len(sq) <= max_seq_len:
                # find m/z ratio
                sp_d = spectrum.split('\n')[4:]  # get to the actual spectrum data, post comment
                sq_lst.append([i, sq])

                # add m/z and intensity binned (int) into list of lists (append) --> data

                for j, spectrum_data in enumerate(sp_d):
                    mz = int(float(spectrum_data.split('\t')[0]))

                    # select m/z ration to fit reqs
                    if mz_min <= mz <= mz_max:
                        # print(mz)

                        it = int(float(spectrum_data.split('\t')[1]))
                        cols.append(i)  # if it looks weird try j

                        mz_a = 0  # maybe default None
                        it_a = 0
                        if mz == mz_a:
                            if it > it_a:
                                data.pop(-1)
                                data.append([i, mz, it])
                                # it_lst.pop(-1)
                                # it_lst.append(it)
                                # frame.loc[i, mz] = it
                                it_a = it
                        else:
                            data.append([i, mz, it])
                            # mz_lst.append(mz)
                            # it_lst.append(it)
                            # frame.loc[i, mz] = it
                            mz_a = mz  # achieved values to compare new ones
                            it_a = it
        # big_df = pd.DataFrame()
        # # big_df.loc[i] = it_lst
        # big_df.append(it_lst)

    # df = pd.DataFrame(data)  # , index=[0], columns=[1])  # .T.dropna(how='all').fillna(0)
    # todo: put inplace=True

    # help_df = pd.DataFrame(data).rename(columns={0: 'spectra', 1: 'mz', 2: 'it'})

    df = data
    seqs = pd.DataFrame(sq_lst).set_index(0).rename(columns={1: 'sequence'})  # , inplace=True)  # todo: check and set

    return df, seqs


if __name__ == '__main__':
    input_file = 'C:/Users/laura/PycharmProjects/fufezan-lab-advanced_python_2020-21_HD_fork/data' \
                 '/cptac2_mouse_hcd_selected_copy.msp'
    r = msp_to_df(input_file)
    print('dataframe \n', r[0])
    print('sequence \n', r[1])
