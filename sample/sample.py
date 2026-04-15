import json

logs = [
   {
      "behaviorName":"PresentMenuAndAcceptUserChoice",
      "stmtId":"ea8a2ba6-cef8-4567-bcb8-6cc367b83d27",
      "type":"behavior"
   },
   {
      "behaviorName":"PresentMenuAndAcceptUserChoice",
      "stmtId":"30f9234b-05a0-44cb-afce-9bd116a28662",
      "type":"behavior"
   },
   {
      "behaviorName":"PresentMenuAndAcceptUserChoice",
      "stmtId":"02f9d50e-1c78-4abc-a7b5-0597c5e25702",
      "type":"behavior"
   },
   {
      "behaviorName":"PresentMenuAndAcceptUserChoice",
      "participantName":"respomse",
      "participantValue":"a",
      "stmtId":"02f9d50e-1c78-4abc-a7b5-0597c5e25702",
      "type":"participant"
   },
   {
      "behaviorName":"AcceptBook",
      "stmtId":"cb28f429-9569-41e1-a14c-7fdfeb118973",
      "type":"behavior"
   },
   {
      "behaviorName": "AcceptBook",
      "stmtId": "2a54eede-12e4-4b78-9d4e-f28fe1802518",
      "type": "behavior"
   },
   {
      "behaviorName": "AcceptBook",
      "stmtId": "b521816b-ac27-4cac-a767-a4c62ea4b6b1",
      "type": "behavior"
   },
   {
      "behaviorName": "AcceptBook",
      "stmtId": "c0265dcf-f3e3-4dfb-a60d-f7e217d81638",
      "type": "behavior"
   },
   {
      "behaviorName": "AcceptBook",
      "participantName": "book",
      "participantValue": {
         "genre": "GENRE1",
         "name": "BOOK1"
      },
      "stmtId": "c0265dcf-f3e3-4dfb-a60d-f7e217d81638",
      "type": "participant"
   },
   {
      "behaviorName": "PlaceBookInBasket",
      "stmtId": "f6d5ddd6-7de1-4647-b213-cd07293e8624",
      "type": "behavior"
   },
   {
      "behaviorName": "PresentMenuAndAcceptUserChoice",
      "stmtId": "ea8a2ba6-cef8-4567-bcb8-6cc367b83d27",
      "type": "behavior"
   }
]

class TraceWalker:

   def __init__ (self):
      print("initialized")
      self.position = None
      self.invariantsViolated = []
      self.summary = None

   def b_AcceptLogs(self, logs):
      self.logs = logs

   def b_SetInitialPosition(self):
      self.position = 0

   def b_GetLogAtCurrentPosition(self, logs, position):
      self.currentLog = logs[position]

   def b_GetCurrentPositionType(self, currentLog):
      self.currType = currentLog["type"]

   def b_GetParticipantNameAndValue(self, currentLog):
      return {
         "participantName": currentLog["participantName"], 
         "participantValue": currentLog["participantValue"]
      }

   def b_GetValidTransitionsOfCurrentPosition(self):
      return []

   def b_GetBehaviorOfCurrentPosition(self, currentLog):
      return currentLog["behaviorName"]

   def b_EnforceInvariant(self, name, value):
      return True

   def b_SaveInvariantViolation(self, currentLog, invariantViolated):
      self.invariantsViolated.append({
         "log": currentLog,
         "invariantViolated": invariantViolated
      })

   def b_AdvancePosition(self, position):
      self.position = position + 1

   def b_SaveSummaryOfWalk(self, invariantsViolated):
      self.summary = "Walk Finished with " + str(len(invariantsViolated)) + " invariants violated"

   def b_GetBehaviorOfNextPosition(self, position):
      return self.logs[position + 1]["behaviorName"]

   def b_GetLogOfNextPosition(self, position):
      return self.logs[position + 1]

   def b_SaveInstrumentationFailure(self):
      self.instrumentationFailure = True

   def run(self,logs):
      self.b_AcceptLogs(logs)
      self.b_SetInitialPosition()
      
      while self.position < len(self.logs):
         self.b_GetLogAtCurrentPosition(self.logs, self.position)
         self.b_GetCurrentPositionType(self.currentLog)

         # Process Participant
         if (self.currType == "participant"):
            obj = self.b_GetParticipantNameAndValue(self.currentLog)
            result = self.b_EnforceInvariant(obj["participantName"], obj["participantValue"])
            if result:
               self.b_SaveInvariantViolation(self.currentLog, result)

         # Check if we still in the same behavior
         currBehavior = self.b_GetBehaviorOfCurrentPosition(self.currentLog)

         if (self.position + 1 >= len(self.logs)):
            break

         nextBehavior = self.b_GetBehaviorOfNextPosition(self.position)
         if (currBehavior == nextBehavior):
            self.b_AdvancePosition(self.position)
            continue

         # Check valid transition, advance or save instrumentation failure
         validTransitions = self.b_GetValidTransitionsOfCurrentPosition()
         # Simulating always valid transition
         if (True or nextBehavior in validTransitions):
            self.b_AdvancePosition(self.position)
         else:
            self.b_SaveInstrumentationFailure()
            break

         self.b_AdvancePosition(self.position)

      self.b_SaveSummaryOfWalk(self.invariantsViolated)
      print(self.summary)

if __name__ == "__main__":
   w = TraceWalker()
   w.run(logs)