"""Four original waiting-slot index helpers over explicit inherited buffers.

This is not PostSound/Manage queue reconstruction. Request records, sorting,
transfers, COM/DirectSound and physical buffers remain outside this provider.
"""
import struct
from bancos_som import DependenciaSom


class WaitingSlotIndex:
    """Live u32 at 0x498f68 and the first 20 x 44 bytes at 0x52137c.

    Keep the supplied writable objects by identity. No state is allocated,
    initialized or defaulted; writes are in place, and there are no callbacks.
    """
    def __init__(self, index_word, playing_table):
        self._check_buffer(index_word,4,'waiting maximum-index word')
        self._check_buffer(playing_table,20*44,'playing-record table')
        self.index_word=index_word
        self.playing_table=playing_table

    @staticmethod
    def _check_buffer(buffer,size,name):
        try:view=memoryview(buffer)
        except TypeError as exc:raise ValueError(name+' must be a writable byte buffer') from exc
        if view.readonly or view.ndim!=1 or not view.c_contiguous or view.itemsize!=1 or view.nbytes!=size:
            raise ValueError(name+' must be a writable contiguous byte buffer of '+str(size)+' bytes')

    def maximum(self):
        """WaitSnd_GetMaxIndice 0x48afe9: the raw inherited u32, without mutation."""
        return struct.unpack('<I',self.index_word)[0]

    def _supported_index(self,address):
        index=self.maximum()
        if not 19<=index<=70:
            raise DependenciaSom(address,'waiting maximum index outside the verified 19..70 queue domain')
        return index

    def reserve(self):
        """WaitSnd_GetFirstFreePlace 0x48aef8: next index, or u32 -1 at 70."""
        index=self._supported_index(0x48aefa)
        if index==70:return 0xffffffff
        index+=1
        struct.pack_into('<I',self.index_word,0,index)
        return index

    def give_back(self):
        """WaitSnd_SorryGiveBackOnePlace 0x48afd0; EAX is preserved, no API result."""
        index=self._supported_index(0x48afd2)
        if index!=19:struct.pack_into('<I',self.index_word,0,index-1)

    def find_place(self):
        """WaitSnd_FindPlace 0x48afef: first +8 status byte equal to zero, 0..19."""
        for index in range(20):
            if memoryview(self.playing_table).cast('B')[index*44+8]==0:return index
        return 0xffffffff
